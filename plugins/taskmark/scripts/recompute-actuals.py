#!/usr/bin/env python3
"""Recompute Taskmark actual_minutes / actual_ms and parent rollups.

actual_ms       = billable Work log sessions in milliseconds (idle + session caps;
                  shared-batch redistribution; commit-span recovery)
actual_minutes  = floor(actual_ms / 60000)

Sizing suggests **t-shirt size + story points only**. Velocity / time-estimate
calibration was removed (board S-057). `estimate_minutes` may still roll up from
children for historical INDEX columns but is not suggested or calibrated here.

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
    dt = dt.astimezone(timezone.utc)
    ms = dt.microsecond // 1000
    if ms:
        return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{ms:03d}Z"
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def idle_deadline(started: datetime) -> datetime:
    d = started.astimezone(timezone.utc).date() + timedelta(days=1)
    return datetime(d.year, d.month, d.day, 12, 0, 0, tzinfo=timezone.utc)


def billable_ms(
    started: datetime, ended: datetime | None, session_cap: int, now: datetime
) -> int:
    """Billable duration in milliseconds (idle + session caps)."""
    if ended is None:
        end_eff = now
    else:
        end_eff = ended
    idle = idle_deadline(started)
    cap_end = started + timedelta(minutes=session_cap)
    billable_end = min(end_eff, idle, cap_end)
    ms = math.floor((billable_end - started).total_seconds() * 1000)
    return max(0, ms)


def billable_minutes(
    started: datetime, ended: datetime | None, session_cap: int, now: datetime
) -> int:
    return billable_ms(started, ended, session_cap, now) // 60_000


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


def worklog_billable_ms(sessions: list[Session], cap: int, now: datetime) -> int:
    return sum(billable_ms(s.started, s.ended, cap, now) for s in sessions)


def worklog_billable(sessions: list[Session], cap: int, now: datetime) -> int:
    return worklog_billable_ms(sessions, cap, now) // 60_000


def own_actual_ms(item: Item, now: datetime) -> int:
    return worklog_billable_ms(item.sessions, session_cap(item.fm), now)


def own_actual(item: Item, now: datetime) -> int:
    """Billable minutes from Work log sessions (start-work → complete-work)."""
    return own_actual_ms(item, now) // 60_000


def allocate_by_weights(total: int, weights: list[int]) -> list[int]:
    """Largest-remainder allocation so parts sum exactly to total."""
    n = len(weights)
    if n == 0:
        return []
    if total <= 0:
        return [0] * n
    safe = [max(0, int(w)) for w in weights]
    if sum(safe) <= 0:
        safe = [1] * n
    wsum = sum(safe)
    raw = [total * w / wsum for w in safe]
    floors = [math.floor(x) for x in raw]
    rem = total - sum(floors)
    order = sorted(
        range(n),
        key=lambda i: (raw[i] - floors[i], safe[i], -i),
        reverse=True,
    )
    for i in order[:rem]:
        floors[i] += 1
    return floors


def item_weight(item: Item) -> int:
    try:
        pts = int(item.fm.get("points") or 0)
    except ValueError:
        pts = 0
    if pts > 0:
        return pts
    try:
        est = int(item.fm.get("estimate_minutes") or 0)
    except ValueError:
        est = 0
    return max(1, est) if est > 0 else 1


def redistribute_shared_batch_sessions(items: list[Item], now: datetime) -> int:
    """Split identical parallel leaf sessions so one wall-clock batch is not counted N times.

    When 2+ task/bug leaves under the same epic share the same closed (Started, Ended),
    treat that span as one shared batch: allocate billable **milliseconds** by points (else
    estimate_minutes) with largest-remainder, rewrite each leaf Ended to
    Started + allocated, and zero matching parent story/epic sessions so rollup
    Actual equals the batch total.
    """
    by_id = {i.fm.get("id"): i for i in items if i.fm.get("id")}
    leaves = [i for i in items if i.fm.get("type") in {"task", "bug"}]

    # epic_id -> list of leaves
    by_epic: dict[str, list[Item]] = {}
    for leaf in leaves:
        epic_id = (leaf.fm.get("epic") or "").strip()
        if not epic_id or epic_id in {"null", "None"}:
            # fall back to parent story's epic
            parent = by_id.get((leaf.fm.get("parent") or "").strip())
            if parent:
                epic_id = (parent.fm.get("epic") or parent.fm.get("id") or "").strip()
        if not epic_id or epic_id in {"null", "None"}:
            continue
        by_epic.setdefault(epic_id, []).append(leaf)

    changed = 0
    batch_keys: set[tuple[str, str]] = set()  # (started_iso, ended_iso)

    for epic_id, epic_leaves in by_epic.items():
        # group (leaf, session_index) by (started, ended)
        groups: dict[tuple[datetime, datetime], list[tuple[Item, int]]] = {}
        for leaf in epic_leaves:
            for idx, sess in enumerate(leaf.sessions):
                if sess.ended is None:
                    continue
                # Already proportionally allocated — do not re-split
                if "shared-batch:" in (sess.summary or ""):
                    continue
                key = (sess.started, sess.ended)
                groups.setdefault(key, []).append((leaf, idx))

        for (started, ended), members in groups.items():
            # unique leaves only (one session per leaf in this batch)
            uniq: dict[str, tuple[Item, int]] = {}
            for leaf, idx in members:
                lid = leaf.fm.get("id") or str(leaf.path)
                # prefer first matching session
                if lid not in uniq:
                    uniq[lid] = (leaf, idx)
            if len(uniq) < 2:
                continue

            # Only redistribute when the parallel copy would inflate (same full span)
            cap = max(session_cap(m[0].fm) for m in uniq.values())
            total_ms = billable_ms(started, ended, cap, now)
            if total_ms <= 0:
                continue

            ordered = sorted(uniq.values(), key=lambda t: t[0].fm.get("id") or "")
            weights = [item_weight(leaf) for leaf, _ in ordered]
            allocs = allocate_by_weights(total_ms, weights)
            start_iso = fmt_ts(started)
            end_iso = fmt_ts(ended)
            batch_keys.add((start_iso, end_iso))

            for (leaf, idx), ms in zip(ordered, allocs):
                sess = leaf.sessions[idx]
                new_ended = started + timedelta(milliseconds=ms)
                note = f"shared-batch: {ms} of {total_ms}ms by points"
                summary = sess.summary
                if "shared-batch:" not in summary:
                    summary = f"{summary}; {note}" if summary else note
                else:
                    summary = re.sub(
                        r"shared-batch:.*?by points",
                        note,
                        summary,
                    )
                leaf.sessions[idx] = Session(
                    num=sess.num,
                    actor=sess.actor,
                    started=started,
                    ended=new_ended,
                    summary=summary,
                )
                leaf.text = replace_work_log_rows(leaf.text, leaf.sessions)
                leaf.text = set_frontmatter(leaf.text, {"updated": fmt_ts(now)})
                changed += 1

    if not batch_keys:
        return changed

    # Zero parent story/epic sessions that duplicated the full batch span
    for item in items:
        if item.fm.get("type") not in {"story", "epic"}:
            continue
        mutated = False
        for idx, sess in enumerate(item.sessions):
            if sess.ended is None:
                continue
            if "shared-batch:" in (sess.summary or ""):
                continue
            key = (fmt_ts(sess.started), fmt_ts(sess.ended))
            if key not in batch_keys:
                continue
            summary = sess.summary
            note = "shared-batch: 0ms rollup (children hold allocation)"
            if "shared-batch:" not in summary:
                summary = f"{summary}; {note}" if summary else note
            item.sessions[idx] = Session(
                num=sess.num,
                actor=sess.actor,
                started=sess.started,
                ended=sess.started,  # 0 billable
                summary=summary,
            )
            mutated = True
        if mutated:
            item.text = replace_work_log_rows(item.text, item.sessions)
            item.text = set_frontmatter(item.text, {"updated": fmt_ts(now)})
            changed += 1

    return changed


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
    """Attach children via parent id; epic-direct leaves also attach via epic.

    Tasks/bugs may have ``parent: null`` (or a missing parent) while still setting
    ``epic: E-NNN``. Those must hang under the epic so points/estimates roll up.
    """
    by_id = {i.fm["id"]: i for i in items if i.fm.get("id")}
    for item in items:
        parent_id = (item.fm.get("parent") or "").strip()
        if parent_id in {"", "null", "None", "—", "-"}:
            parent_id = ""
        if parent_id and parent_id in by_id:
            by_id[parent_id].children.append(item)
            continue
        # Fallback: attach story / leaf to epic when parent is missing or unknown
        if item.fm.get("type") in {"task", "bug", "story"}:
            epic_id = (item.fm.get("epic") or "").strip()
            if epic_id in {"", "null", "None", "—", "-"}:
                epic_id = ""
            if epic_id and epic_id in by_id and epic_id != item.fm.get("id"):
                by_id[epic_id].children.append(item)


def median_or_none(vals: list[int]) -> int | None:
    if not vals:
        return None
    return int(round(statistics.median(vals)))



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



def rollup_parent(item: Item, now: datetime) -> None:
    """Roll points/estimate from children; actual = max(sum children, own sessions).

    - Story points = sum of child task/bug points; size rolls from child t-shirts.
    - Epic points = sum of child story points **and** epic-direct task/bug points;
      epic has **no** t-shirt size.
    """
    if not item.children:
        # Clear stale rolled-up totals when all children are gone (e.g. moved/deleted).
        if item.fm.get("type") in {"story", "epic"} and item.fm.get("points_source") == "rolled_up":
            updates: dict[str, Any] = {
                "points": 0,
                "estimate_minutes": 0,
                "points_source": "rolled_up",
                "updated": fmt_ts(now),
            }
            if item.fm.get("type") == "epic":
                updates["size"] = None
                updates["size_source"] = "rolled_up"
                updates["size_basis"] = "[sum:children]"
                updates["estimate_source"] = "rolled_up"
                updates["estimate_basis"] = "[sum:children]"
            item.fm.update({k: ("null" if v is None else str(v)) for k, v in updates.items()})
            item.text = set_frontmatter(item.text, updates, drop_keys=["effort_minutes"])
        return
    est = sum(int(c.fm.get("estimate_minutes") or 0) for c in item.children)
    points = sum(int(c.fm.get("points") or 0) for c in item.children)
    child_ms = sum(int(c.fm.get("actual_ms") or 0) for c in item.children)
    # Fallback for children not yet migrated to actual_ms
    if child_ms == 0:
        child_ms = sum(int(c.fm.get("actual_minutes") or 0) * 60_000 for c in item.children)
    own_ms = own_actual_ms(item, now)
    actual_ms = max(child_ms, own_ms)
    actual = actual_ms // 60_000
    updates = {
        "estimate_minutes": est,
        "points": points,
        "points_source": "rolled_up",
        "actual_minutes": actual,
        "actual_ms": actual_ms,
        "updated": fmt_ts(now),
    }
    if item.fm.get("type") == "epic":
        updates["size"] = None
        updates["size_source"] = "rolled_up"
        updates["size_basis"] = "[sum:children]"
        updates["estimate_source"] = "rolled_up"
        updates["estimate_basis"] = "[sum:children]"
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



def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("taskmark", type=Path, help="Path to Taskmark board root")
    ap.add_argument("--calibrate", action="store_true", help="Reserved flag (time-estimate calibration removed; still rolls up actuals)")
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

    # After commit-span recovery: split any identical parallel leaf spans
    shared_batch = redistribute_shared_batch_sessions(items, now)

    started_recovered = 0
    for item in items:
        if ensure_started_at_from_sessions(item):
            started_recovered += 1
            item.text = set_frontmatter(
                item.text, {"started_at": item.fm["started_at"], "updated": fmt_ts(now)}
            )

    for item in items:
        actual_ms = own_actual_ms(item, now)
        actual = actual_ms // 60_000
        item.fm["actual_minutes"] = str(actual)
        item.fm["actual_ms"] = str(actual_ms)
        # Drop legacy effort_minutes; Actual is session time only
        item.text = set_frontmatter(
            item.text,
            {
                "actual_minutes": actual,
                "actual_ms": actual_ms,
                "updated": fmt_ts(now),
            },
            drop_keys=["effort_minutes"],
        )

    for item in items:
        if item.fm.get("type") == "story":
            rollup_parent(item, now)
    for item in items:
        if item.fm.get("type") == "epic":
            rollup_parent(item, now)

    if args.calibrate:
        # Time-estimate / velocity calibration removed (S-057). Flag kept for callers.
        print("calibrate: skipped time-estimate/velocity calibration (removed)")

    for item in items:
        if not args.dry_run:
            item.path.write_text(item.text, encoding="utf-8")

    refresh_index_actuals(taskmark, by_id, args.dry_run)

    print(f"taskmark: {taskmark}")
    print(
        f"items: {len(items)}; shared-batch redistributed: {shared_batch}; "
        f"recovered commit-span: {recovered}; "
        f"started_at from sessions: {started_recovered}"
    )
    for item in sorted(items, key=lambda i: i.fm["id"]):
        print(
            f"  {item.fm['id']} type={item.fm.get('type')} "
            f"actual={item.fm.get('actual_minutes')} "
            f"actual_ms={item.fm.get('actual_ms')} "
            f"est={item.fm.get('estimate_minutes')} "
            f"size={item.fm.get('size')} points={item.fm.get('points')}"
        )
    if args.dry_run:
        print("(dry-run: no files written)")


if __name__ == "__main__":
    main()
