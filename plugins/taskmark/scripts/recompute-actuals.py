#!/usr/bin/env python3
"""Recompute Taskmark actual_minutes and estimates.

actual_minutes  = billable Work log sessions from start-work → complete-work
                  (idle + session caps; commit-span recovery)
estimate_minutes = points × 30-day median min/point (on create / calibrate),
                  else SIZING seeds

Usage:
  python3 recompute-actuals.py /path/to/board
  python3 recompute-actuals.py /path/to/board --calibrate
  python3 recompute-actuals.py /path/to/board --dry-run
"""

from __future__ import annotations

import argparse
import math
import re
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

DASH_ENDED = {"—", "-", "–", ""}

SIZE_WEIGHT = {"XS": 1, "S": 2, "M": 3, "L": 4, "XL": 5}
WEIGHT_TO_SIZE = [(1, "XS"), (3, "S"), (6, "M"), (10, "L"), (10**9, "XL")]
SIZE_POINTS = {"XS": 1, "S": 2, "M": 3, "L": 5, "XL": 8}
DEFAULT_SEEDS = {"XS": 30, "S": 120, "M": 480, "L": 960, "XL": 1440}
VELOCITY_WINDOW_DAYS = 30
MIN_VELOCITY_SAMPLES = 3

FM_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
WORK_LOG_RE = re.compile(
    r"(## Work log\n\n\| Session \| Actor \| Started \(UTC\) \| Ended \(UTC\) \| Summary \|\n"
    r"\|---------+\|-------+\|---------------+\|-------------+\|---------+\|\n)"
    r"((?:\|.*\n)*)",
    re.MULTILINE,
)
COMMITS_RE = re.compile(
    r"(## Commits\n\n\| SHA \| Repo \| Date \(UTC\) \| Message \|\n"
    r"\|-----+\|------+\|------------+\|---------+\|\n)"
    r"((?:\|.*\n)*)",
    re.MULTILINE,
)
SESSION_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*(.*?)\s*\|\s*$"
)
COMMIT_ROW_RE = re.compile(
    r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$"
)


def parse_ts(s: str) -> datetime | None:
    s = s.strip()
    if not s or s in DASH_ENDED:
        return None
    if s.endswith("Z"):
        try:
            return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def fmt_ts(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def idle_deadline(started: datetime) -> datetime:
    d = started.astimezone(timezone.utc).date() + timedelta(days=1)
    return datetime(d.year, d.month, d.day, 12, 0, 0, tzinfo=timezone.utc)


def billable_minutes(
    started: datetime, ended: datetime | None, session_cap: int, now: datetime
) -> int:
    if ended is None:
        end_eff = now
    else:
        end_eff = ended
    idle = idle_deadline(started)
    cap_end = started + timedelta(minutes=session_cap)
    billable_end = min(end_eff, idle, cap_end)
    mins = math.floor((billable_end - started).total_seconds() / 60)
    return max(0, mins)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    m = FM_RE.match(text)
    if not m:
        return {}, text
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[m.end() :]


def set_frontmatter(text: str, updates: dict[str, Any], *, drop_keys: list[str] | None = None) -> str:
    m = FM_RE.match(text)
    if not m:
        return text
    body = m.group(1).rstrip() + "\n"
    for k, v in updates.items():
        val = "null" if v is None else str(v)
        if re.search(rf"^{re.escape(k)}:", body, re.M):
            body = re.sub(rf"^{re.escape(k)}:.*$", f"{k}: {val}", body, count=1, flags=re.M)
        else:
            body += f"{k}: {val}\n"
    for k in drop_keys or []:
        body = re.sub(rf"^{re.escape(k)}:.*\n", "", body, flags=re.M)
    rest = text[m.end() :]
    if rest.startswith("\n"):
        return f"---\n{body}---{rest}"
    return f"---\n{body}---\n\n{rest}"


@dataclass
class Session:
    num: int
    actor: str
    started: datetime
    ended: datetime | None
    summary: str


@dataclass
class Item:
    path: Path
    text: str
    fm: dict[str, str]
    sessions: list[Session] = field(default_factory=list)
    commit_times: list[datetime] = field(default_factory=list)
    children: list["Item"] = field(default_factory=list)


def parse_sessions(text: str) -> list[Session]:
    m = WORK_LOG_RE.search(text)
    if not m:
        return []
    sessions: list[Session] = []
    for line in m.group(2).splitlines():
        row = SESSION_ROW_RE.match(line.strip())
        if not row:
            continue
        started = parse_ts(row.group(3))
        if not started:
            continue
        ended_raw = row.group(4).strip()
        ended = None if ended_raw in DASH_ENDED else parse_ts(ended_raw)
        sessions.append(
            Session(
                num=int(row.group(1)),
                actor=row.group(2).strip(),
                started=started,
                ended=ended,
                summary=row.group(5).strip(),
            )
        )
    return sessions


def parse_commit_times(text: str) -> list[datetime]:
    m = COMMITS_RE.search(text)
    if not m:
        return []
    times: list[datetime] = []
    for line in m.group(2).splitlines():
        row = COMMIT_ROW_RE.match(line.strip())
        if not row:
            continue
        sha = row.group(1).strip()
        if sha in {"—", "-", "–"}:
            continue
        ts = parse_ts(row.group(3))
        if ts:
            times.append(ts)
    return times


def replace_work_log_rows(text: str, sessions: list[Session]) -> str:
    m = WORK_LOG_RE.search(text)
    if not m:
        return text
    lines = []
    for s in sorted(sessions, key=lambda x: x.num):
        ended = "—" if s.ended is None else fmt_ts(s.ended)
        lines.append(
            f"| {s.num} | {s.actor} | {fmt_ts(s.started)} | {ended} | {s.summary} |"
        )
    body = "\n".join(lines) + ("\n" if lines else "")
    return text[: m.start(2)] + body + text[m.end(2) :]


def session_cap(fm: dict[str, str]) -> int:
    try:
        return int(fm.get("session_cap_minutes") or "480")
    except ValueError:
        return 480


def worklog_billable(sessions: list[Session], cap: int, now: datetime) -> int:
    return sum(billable_minutes(s.started, s.ended, cap, now) for s in sessions)


def own_actual(item: Item, now: datetime) -> int:
    """Billable minutes from Work log sessions (start-work → complete-work)."""
    return worklog_billable(item.sessions, session_cap(item.fm), now)


def ensure_started_at_from_sessions(item: Item) -> bool:
    """If completed/done without started_at, recover from earliest work-log session."""
    if parse_ts(item.fm.get("started_at") or ""):
        return False
    if not item.sessions:
        return False
    status = item.fm.get("status", "")
    completed = parse_ts(item.fm.get("completed_at") or "")
    if status != "done" and not completed:
        return False
    first = min(s.started for s in item.sessions)
    item.fm["started_at"] = fmt_ts(first)
    return True


def maybe_recover_commit_span(item: Item, now: datetime) -> bool:
    """Insert/extend a recovery session if commits span >> work-log billable (effort only)."""
    times = sorted(item.commit_times)
    if not times:
        return False

    started_at = parse_ts(item.fm.get("started_at") or "")
    if len(times) < 2 and not (len(times) == 1 and started_at and started_at < times[0]):
        return False

    first = times[0]
    if started_at and started_at < first:
        first = started_at
    last = times[-1]
    span_min = math.floor((last - first).total_seconds() / 60)
    if span_min < 10:
        return False

    cap = session_cap(item.fm)
    current = worklog_billable(item.sessions, cap, now)
    if current >= max(1, math.floor(span_min * 0.5)):
        return False

    recovered = [s for s in item.sessions if "auto-recovered: commit span" in s.summary]
    if recovered:
        s = recovered[0]
        s.started = min(s.started, first)
        s.ended = max(s.ended or last, last)
        if "auto-recovered: commit span" not in s.summary:
            s.summary = f"{s.summary}; auto-recovered: commit span".strip("; ")
    else:
        next_num = max((s.num for s in item.sessions), default=0) + 1
        item.sessions.append(
            Session(
                num=next_num,
                actor="agent",
                started=first,
                ended=last,
                summary="auto-recovered: commit span",
            )
        )
    return True


def size_from_weight(weight: int) -> str:
    for max_w, size in WEIGHT_TO_SIZE:
        if weight <= max_w:
            return size
    return "XL"


def size_for_actual(actual: int, seeds: dict[str, int]) -> str:
    best = "XS"
    best_diff = 10**9
    for size in ("XS", "S", "M", "L", "XL"):
        seed = seeds.get(size, DEFAULT_SEEDS[size])
        diff = abs(seed - actual)
        if diff < best_diff or (diff == best_diff and SIZE_WEIGHT[size] < SIZE_WEIGHT[best]):
            best = size
            best_diff = diff
    return best


def load_items(taskmark: Path) -> list[Item]:
    items: list[Item] = []
    for path in sorted(taskmark.rglob("*.md")):
        if path.name in {"INDEX.md", "README.md", "SIZING.md", "VELOCITY.md", "REPOS.md"}:
            continue
        if "examples" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        if not fm.get("id") or not fm.get("type"):
            continue
        items.append(
            Item(
                path=path,
                text=text,
                fm=fm,
                sessions=parse_sessions(text),
                commit_times=parse_commit_times(text),
            )
        )
    return items


def build_tree(items: list[Item]) -> None:
    by_id = {i.fm["id"]: i for i in items}
    for item in items:
        parent_id = item.fm.get("parent")
        if parent_id and parent_id != "null" and parent_id in by_id:
            by_id[parent_id].children.append(item)


def median_or_none(vals: list[int]) -> int | None:
    if not vals:
        return None
    return int(round(statistics.median(vals)))


def velocity_ratios(leaves: list[Item], now: datetime) -> list[float]:
    """Trustworthy actual/points ratios for done leaves in the rolling 30-day window."""
    cutoff = now - timedelta(days=VELOCITY_WINDOW_DAYS)
    samples: list[Item] = []
    for i in leaves:
        if i.fm.get("status") != "done" or i.fm.get("type") not in {"task", "bug"}:
            continue
        completed = parse_ts(i.fm.get("completed_at") or "")
        if not completed or completed < cutoff:
            continue
        actual = int(i.fm.get("actual_minutes") or 0)
        points = int(i.fm.get("points") or 0)
        if actual > 2 and points > 0:
            samples.append(i)
    samples.sort(key=lambda x: parse_ts(x.fm.get("completed_at") or "") or now)
    return [
        int(i.fm.get("actual_minutes") or 0) / int(i.fm.get("points") or 1)
        for i in samples
    ]


def median_min_per_point(leaves: list[Item], now: datetime) -> int | None:
    ratios = velocity_ratios(leaves, now)
    if len(ratios) < MIN_VELOCITY_SAMPLES:
        return None
    return int(round(statistics.median(ratios)))


def window_done_leaves(leaves: list[Item], now: datetime) -> list[Item]:
    cutoff = now - timedelta(days=VELOCITY_WINDOW_DAYS)
    out: list[Item] = []
    for i in leaves:
        if i.fm.get("status") != "done" or i.fm.get("type") not in {"task", "bug"}:
            continue
        completed = parse_ts(i.fm.get("completed_at") or "")
        if completed and completed >= cutoff:
            out.append(i)
    out.sort(key=lambda x: parse_ts(x.fm.get("completed_at") or "") or now)
    return out


def update_sizing_md(
    sizing_path: Path,
    seeds: dict[str, int],
    calibration_rows: list[str],
    dry_run: bool,
) -> None:
    if not sizing_path.exists():
        return
    text = sizing_path.read_text(encoding="utf-8")
    for size, mins in seeds.items():
        if mins >= 480:
            seed_label = f"{mins // 480} day ({mins} min)" if mins == 480 else f"{mins} min"
            if size == "L":
                seed_label = f"{mins // 60}h ({mins} min)" if mins < 960 else f"{mins // 480} days"
            if size == "XL":
                seed_label = f"{mins}+ min (prefer split)" if mins < 1440 else "3+ days"
        elif mins >= 60:
            seed_label = f"{mins // 60} h ({mins} min)" if mins % 60 == 0 else f"{mins} min"
        else:
            seed_label = f"{mins} min"

        pattern = rf"(\| {size} \| \d+ \| [^|]+ \| )[^|\n]+(\|)"
        text2, n = re.subn(pattern, rf"\g<1>{seed_label} \2", text, count=1)
        if n:
            text = text2

    if calibration_rows:
        cal_header = re.search(
            r"(\| Date \| Item \| Sized \| Points \| Est \| Actual \| Note \|\n"
            r"\|------+\|------+\|-------+\|--------+\|-----+\|--------+\|------+\|\n)",
            text,
        )
        if cal_header:
            insert_at = cal_header.end()
            rest = text[insert_at:]
            rest = re.sub(r"^\| — \| — \| — \| — \| — \| — \| — \|\n", "", rest)
            new_rows = "".join(r + "\n" for r in calibration_rows)
            text = text[:insert_at] + new_rows + rest

    if "effort_minutes" not in text and "billable-session" in text:
        text = text.replace(
            "Effort uses **billable work-log minutes** only",
            "Velocity and calibration use **effort_minutes** (billable work-log). "
            "`actual_minutes` is wall-clock start→complete. "
            "Effort uses **billable work-log minutes** only",
            1,
        )

    if not dry_run:
        sizing_path.write_text(text, encoding="utf-8")


def refresh_index_actuals(taskmark: Path, by_id: dict[str, Item], dry_run: bool) -> None:
    index = taskmark / "INDEX.md"
    if not index.exists():
        return
    text = index.read_text(encoding="utf-8")
    lines_out: list[str] = []
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if (
            not stripped.startswith("| ")
            or stripped.startswith("|----")
            or stripped.startswith("| ID ")
            or stripped.startswith("| Item ")
        ):
            lines_out.append(line)
            continue
        parts = [p.strip() for p in stripped.strip("|").split("|")]
        if not parts:
            lines_out.append(line)
            continue
        iid = parts[0]
        if iid not in by_id:
            lines_out.append(line)
            continue
        item = by_id[iid]
        if len(parts) == 8:
            parts[2] = str(item.fm.get("status", parts[2]))
            # Epics: no t-shirt size — show em dash
            if item.fm.get("type") == "epic":
                size_val = item.fm.get("size") or ""
                parts[3] = "—" if size_val in {"", "null", "None"} else size_val
            else:
                parts[3] = str(item.fm.get("size", parts[3]))
            parts[4] = str(item.fm.get("points", parts[4]))
            parts[5] = str(item.fm.get("estimate_minutes", parts[5]))
            parts[6] = str(item.fm.get("actual_minutes", parts[6]))
        elif len(parts) >= 9:
            parts[3] = str(item.fm.get("status", parts[3]))
            parts[4] = str(item.fm.get("size", parts[4]))
            parts[5] = str(item.fm.get("points", parts[5]))
            parts[6] = str(item.fm.get("estimate_minutes", parts[6]))
            parts[7] = str(item.fm.get("actual_minutes", parts[7]))
        else:
            lines_out.append(line)
            continue
        rebuilt = "| " + " | ".join(parts) + " |"
        lines_out.append(rebuilt + ("\n" if line.endswith("\n") else ""))
    text = "".join(lines_out)
    now = fmt_ts(datetime.now(timezone.utc))
    text = re.sub(r"Last synced:.*", f"Last synced: {now}", text, count=1)
    if not dry_run:
        index.write_text(text, encoding="utf-8")


def refresh_velocity(taskmark: Path, leaves: list[Item], now: datetime, dry_run: bool) -> None:
    vel = taskmark / "VELOCITY.md"
    if not vel.exists():
        return
    done = window_done_leaves(leaves, now)
    trustworthy = [i for i in done if int(i.fm.get("actual_minutes") or 0) > 2]
    points = [int(i.fm.get("points") or 0) for i in trustworthy]
    actuals = [int(i.fm.get("actual_minutes") or 0) for i in trustworthy]
    med_ratio = median_min_per_point(leaves, now)

    open_leaves = [
        i
        for i in leaves
        if i.fm.get("type") in {"task", "bug"} and i.fm.get("status") not in {"done", "cancelled"}
    ]
    rem_points = sum(int(i.fm.get("points") or 0) for i in open_leaves)
    rem_est = sum(int(i.fm.get("estimate_minutes") or 0) for i in open_leaves)

    med_points = median_or_none([p for p in points if p > 0])
    med_actual = median_or_none([a for a in actuals if a > 0])

    pts_week = "insufficient data"
    if trustworthy:
        sum_pts = sum(int(i.fm.get("points") or 0) for i in done)
        pts_week = str(round(sum_pts / (VELOCITY_WINDOW_DAYS / 7), 1))

    text = vel.read_text(encoding="utf-8")
    text = re.sub(r"Last synced:.*", f"Last synced: {fmt_ts(now)}", text, count=1)
    text = re.sub(
        r"Window:.*",
        f"Window: rolling {VELOCITY_WINDOW_DAYS} days (done tasks/bugs by completed_at)",
        text,
        count=1,
    )
    # Prefer Est/Actual naming in velocity file
    text = text.replace("| Median effort_minutes |", "| Median actual_minutes |", 1)

    def set_metric(label: str, value: str) -> None:
        nonlocal text
        text = re.sub(
            rf"(\| {re.escape(label)} \| ).*?( \|)",
            rf"\g<1>{value}\2",
            text,
            count=1,
        )

    set_metric("Median actual_minutes", str(med_actual) if med_actual is not None else "—")
    set_metric("Done items in window", str(len(done)))
    set_metric("Sum points", str(sum(int(i.fm.get("points") or 0) for i in done)))
    set_metric("Median points", str(med_points) if med_points is not None else "—")
    set_metric(
        "Median minutes per point",
        str(med_ratio) if med_ratio is not None else "insufficient data",
    )
    set_metric("Points per week (approx)", pts_week)
    set_metric("Open items (excl. cancelled)", str(len(open_leaves)))
    set_metric("Sum points remaining", str(rem_points))
    set_metric("Sum estimate_minutes remaining", str(rem_est))
    if med_ratio and rem_points:
        set_metric("ETA (from median min/point)", f"~{med_ratio * rem_points} min")
    else:
        set_metric(
            "ETA (from median min/point)",
            "insufficient data" if not rem_points else "—",
        )

    note_block = text.split("## Notes")[-1] if "## Notes" in text else ""
    if "session billable" not in note_block:
        text = re.sub(
            r"(## Notes\n\n)",
            r"\1- Speed uses **actual_minutes** (start-work → complete-work sessions) "
            f"over {VELOCITY_WINDOW_DAYS} days. Est = points × median min/point.\n",
            text,
            count=1,
        )

    if not dry_run:
        vel.write_text(text, encoding="utf-8")


def rollup_parent(item: Item, now: datetime) -> None:
    """Roll points/estimate from children; actual = max(sum children, own sessions).

    - Story points = sum of child task/bug points; size rolls from child t-shirts.
    - Epic points = sum of child story points; epic has **no** t-shirt size.
    """
    if not item.children:
        return
    est = sum(int(c.fm.get("estimate_minutes") or 0) for c in item.children)
    points = sum(int(c.fm.get("points") or 0) for c in item.children)
    child_actual = sum(int(c.fm.get("actual_minutes") or 0) for c in item.children)
    actual = max(child_actual, own_actual(item, now))
    updates: dict[str, Any] = {
        "estimate_minutes": est,
        "points": points,
        "points_source": "rolled_up",
        "actual_minutes": actual,
        "updated": fmt_ts(now),
    }
    if item.fm.get("type") == "epic":
        updates["size"] = None
        updates["size_source"] = "rolled_up"
        updates["size_basis"] = "[sum:stories]"
        updates["estimate_basis"] = "[sum:stories]"
    else:
        weight = 0
        for c in item.children:
            sz = (c.fm.get("size") or "").strip()
            if sz in SIZE_WEIGHT:
                weight += SIZE_WEIGHT[sz]
            else:
                pts = int(c.fm.get("points") or 0)
                approx = {1: "XS", 2: "S", 3: "M", 5: "L", 8: "XL"}.get(pts, "M")
                weight += SIZE_WEIGHT[approx]
        updates["size"] = size_from_weight(weight)
        updates["size_source"] = "rolled_up"
        updates["size_basis"] = "[sum:tasks]"
        updates["estimate_basis"] = "[sum:tasks]"
    item.fm.update({k: ("null" if v is None else str(v)) for k, v in updates.items()})
    item.text = set_frontmatter(item.text, updates, drop_keys=["effort_minutes"])


def refresh_suggested_estimates(
    items: list[Item], leaves: list[Item], now: datetime
) -> int:
    """Refresh non-manual leaf estimates from monthly velocity × points."""
    med = median_min_per_point(leaves, now)
    if med is None:
        return 0
    n = 0
    for item in items:
        if item.fm.get("status") in {"done", "cancelled"}:
            continue
        if item.children:
            continue
        if item.fm.get("estimate_source") == "manual":
            continue
        points = int(item.fm.get("points") or 0)
        if points <= 0:
            continue
        new_est = max(5, int(round((med * points) / 5) * 5))
        old = int(item.fm.get("estimate_minutes") or 0)
        if old == new_est:
            continue
        updates = {
            "estimate_minutes": new_est,
            "estimate_basis": f"[velocity:{VELOCITY_WINDOW_DAYS}d:{med}min/pt]",
            "estimate_source": "suggested",
            "updated": fmt_ts(now),
        }
        item.fm.update({k: str(v) for k, v in updates.items()})
        item.text = set_frontmatter(item.text, updates)
        n += 1
    return n


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("taskmark", type=Path, help="Path to Taskmark board root")
    ap.add_argument("--calibrate", action="store_true", help="Recalibrate estimates + SIZING seeds")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    taskmark = args.taskmark.resolve()
    if not taskmark.is_dir():
        raise SystemExit(f"Not a directory: {taskmark}")

    now = datetime.now(timezone.utc)
    items = load_items(taskmark)
    build_tree(items)
    by_id = {i.fm["id"]: i for i in items}
    leaves = [i for i in items if i.fm.get("type") in {"task", "bug"}]

    recovered = 0
    for item in items:
        if maybe_recover_commit_span(item, now):
            recovered += 1
            item.text = replace_work_log_rows(item.text, item.sessions)

    started_recovered = 0
    for item in items:
        if ensure_started_at_from_sessions(item):
            started_recovered += 1
            item.text = set_frontmatter(
                item.text, {"started_at": item.fm["started_at"], "updated": fmt_ts(now)}
            )

    for item in items:
        actual = own_actual(item, now)
        item.fm["actual_minutes"] = str(actual)
        # Drop legacy effort_minutes; Actual is session time only
        item.text = set_frontmatter(
            item.text,
            {
                "actual_minutes": actual,
                "updated": fmt_ts(now),
            },
            drop_keys=["effort_minutes"],
        )

    for item in items:
        if item.fm.get("type") == "story" and item.children:
            rollup_parent(item, now)
    for item in items:
        if item.fm.get("type") == "epic" and item.children:
            rollup_parent(item, now)

    calibration_rows: list[str] = []
    seeds = dict(DEFAULT_SEEDS)
    refreshed = 0

    if args.calibrate:
        by_size: dict[str, list[int]] = {s: [] for s in DEFAULT_SEEDS}
        for item in leaves:
            if item.fm.get("status") != "done":
                continue
            actual = int(item.fm.get("actual_minutes") or 0)
            size = item.fm.get("size", "")
            if actual > 2 and size in by_size:
                by_size[size].append(actual)

        for size, vals in by_size.items():
            med = median_or_none(vals)
            if med is None:
                continue
            if len(vals) >= 5 or (len(vals) >= 3 and len(set(vals)) >= 2):
                seeds[size] = max(5, med)

        today = now.strftime("%Y-%m-%d")
        for item in leaves:
            if item.fm.get("status") != "done":
                continue
            actual = int(item.fm.get("actual_minutes") or 0)
            est = int(item.fm.get("estimate_minutes") or 0)
            if actual <= 2 or est <= 0:
                continue
            ratio = actual / est if est else 0
            if 0.5 <= ratio <= 2:
                continue
            old_size = item.fm.get("size", "M")
            old_points = item.fm.get("points", "3")
            new_est = max(5, int(round(actual / 5) * 5))
            new_size = size_for_actual(actual, seeds)
            new_points = SIZE_POINTS[new_size]
            updates: dict[str, Any] = {
                "estimate_minutes": new_est,
                "estimate_basis": f"[calibrated:{item.fm['id']}]",
                "updated": fmt_ts(now),
            }
            note = f"estimate {est}->{new_est}"
            if new_size != old_size:
                updates["size"] = new_size
                updates["points"] = new_points
                updates["size_source"] = "suggested"
                updates["points_source"] = "suggested"
                updates["size_basis"] = f"[calibrated:{item.fm['id']}]"
                note += f"; size {old_size}->{new_size}"
            item.fm.update({k: str(v) for k, v in updates.items()})
            item.text = set_frontmatter(item.text, updates)
            calibration_rows.append(
                f"| {today} | {item.fm['id']} | {old_size} | {old_points} | {est} | {actual} | {note} |"
            )

        refreshed = refresh_suggested_estimates(items, leaves, now)

        for item in items:
            if item.fm.get("type") == "story" and item.children:
                rollup_parent(item, now)
        for item in items:
            if item.fm.get("type") == "epic" and item.children:
                rollup_parent(item, now)

        update_sizing_md(taskmark / "SIZING.md", seeds, calibration_rows, args.dry_run)

    for item in items:
        if not args.dry_run:
            item.path.write_text(item.text, encoding="utf-8")

    refresh_index_actuals(taskmark, by_id, args.dry_run)
    refresh_velocity(taskmark, leaves, now, args.dry_run)

    print(f"taskmark: {taskmark}")
    print(
        f"items: {len(items)}; recovered commit-span: {recovered}; "
        f"started_at from sessions: {started_recovered}"
    )
    if args.calibrate:
        print(
            f"calibration rows: {len(calibration_rows)}; "
            f"refreshed open estimates: {refreshed}; seeds: {seeds}"
        )
    med = median_min_per_point(leaves, now)
    print(f"velocity median min/point (30d): {med if med is not None else 'insufficient data'}")
    for item in sorted(items, key=lambda i: i.fm["id"]):
        print(
            f"  {item.fm['id']} type={item.fm.get('type')} "
            f"actual={item.fm.get('actual_minutes')} "
            f"est={item.fm.get('estimate_minutes')} "
            f"size={item.fm.get('size')} points={item.fm.get('points')}"
        )
    if args.dry_run:
        print("(dry-run: no files written)")


if __name__ == "__main__":
    main()
