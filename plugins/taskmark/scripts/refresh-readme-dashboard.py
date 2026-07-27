#!/usr/bin/env python3
"""Refresh managed README dashboard sections for a Taskmark board (E-016).

Upserts marker-delimited blocks in board-root README.md:
  - Project status (total / complete / Current Speed)
  - Open work items (stories, tasks, bugs — not done/cancelled/blocked)
  - Changelog (board-repo git commits)

Preserves hand-written intro and the Contributors block.

Usage:
  python3 refresh-readme-dashboard.py /path/to/board
  python3 refresh-readme-dashboard.py /path/to/board --dry-run
  python3 refresh-readme-dashboard.py /path/to/board --changelog-limit 50
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _load_recompute():
    path = Path(__file__).resolve().parent / "recompute-actuals.py"
    spec = importlib.util.spec_from_file_location("recompute_actuals", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    # Required on older Python for dataclasses when loading via importlib
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


STATUS_BEGIN = "<!-- taskmark:project-status:begin -->"
STATUS_END = "<!-- taskmark:project-status:end -->"
OPEN_BEGIN = "<!-- taskmark:open-work:begin -->"
OPEN_END = "<!-- taskmark:open-work:end -->"
CHANGELOG_BEGIN = "<!-- taskmark:changelog:begin -->"
CHANGELOG_END = "<!-- taskmark:changelog:end -->"

SECTION_PATTERNS = {
    "status": re.compile(
        re.escape(STATUS_BEGIN) + r"[\s\S]*?" + re.escape(STATUS_END), re.M
    ),
    "open": re.compile(
        re.escape(OPEN_BEGIN) + r"[\s\S]*?" + re.escape(OPEN_END), re.M
    ),
    "changelog": re.compile(
        re.escape(CHANGELOG_BEGIN) + r"[\s\S]*?" + re.escape(CHANGELOG_END), re.M
    ),
}


def is_truthy_blocked(value: str | None) -> bool:
    return (value or "").strip().lower() in {"true", "yes", "1"}


def format_speed(value: float | None) -> str:
    if value is None:
        return "—"
    rounded = round(value * 10) / 10
    return str(int(rounded)) if float(rounded).is_integer() else f"{rounded:.1f}"


def aggregate_counts(items: list) -> tuple[int, int]:
    total = 0
    complete = 0
    for item in items:
        kind = item.fm.get("type")
        if kind not in {"story", "task", "bug"}:
            continue
        status = (item.fm.get("status") or "").strip().lower()
        if status == "cancelled":
            continue
        total += 1
        if status == "done":
            complete += 1
    return total, complete


def open_work_rows(items: list) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in items:
        kind = item.fm.get("type")
        if kind not in {"story", "task", "bug"}:
            continue
        status = (item.fm.get("status") or "").strip().lower()
        if status in {"done", "cancelled"}:
            continue
        if is_truthy_blocked(item.fm.get("blocked")):
            continue
        size = item.fm.get("size") or "—"
        if size in {"", "null", "None"}:
            size = "—"
        parent = item.fm.get("parent") or ""
        if parent in {"", "null", "None", "—", "-"}:
            parent = item.fm.get("epic") or "—"
        if parent in {"", "null", "None"}:
            parent = "—"
        title = (item.fm.get("title") or "").strip() or "—"
        # Escape pipes in markdown tables
        title = title.replace("|", "\\|")
        rows.append(
            {
                "id": item.fm.get("id") or "—",
                "type": kind,
                "title": title,
                "status": status or "—",
                "size": size,
                "points": str(item.fm.get("points") or "0"),
                "parent": parent,
            }
        )
    rows.sort(key=lambda r: (r["type"], r["id"]))
    return rows


def render_status_block(
    total: int, complete: int, speed: float | None, week_count: int, synced: str
) -> str:
    speed_label = format_speed(speed)
    speed_note = (
        "No completed tasks yet"
        if speed is None
        else f"pts/week · {week_count} active weeks (90d)"
    )
    lines = [
        STATUS_BEGIN,
        "## Project status",
        "",
        f"_Last synced: {synced}_",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total work items | {total} |",
        f"| Complete work items | {complete} |",
        f"| Current speed | {speed_label} ({speed_note}) |",
        "",
        STATUS_END,
    ]
    return "\n".join(lines)


def render_open_work_block(rows: list[dict[str, str]], synced: str) -> str:
    lines = [
        OPEN_BEGIN,
        "## Open work items",
        "",
        f"_Last synced: {synced}_",
        "",
        "Stories, tasks, and bugs that are not done, cancelled, or blocked.",
        "",
    ]
    if not rows:
        lines.append("_No open work items._")
    else:
        lines.extend(
            [
                "| ID | Type | Title | Status | Size | Points | Parent |",
                "|----|------|-------|--------|------|--------|--------|",
            ]
        )
        for r in rows:
            lines.append(
                f"| {r['id']} | {r['type']} | {r['title']} | {r['status']} | "
                f"{r['size']} | {r['points']} | {r['parent']} |"
            )
    lines.extend(["", OPEN_END])
    return "\n".join(lines)


def board_git_log(board: Path, limit: int) -> list[tuple[str, str, str, str]]:
    """Return (sha, iso_date, author, subject) newest first."""
    if not (board / ".git").exists() and not (board / ".git").is_file():
        # may be worktree; still try git -C
        pass
    try:
        out = subprocess.check_output(
            [
                "git",
                "-C",
                str(board),
                "log",
                f"-n{limit}",
                "--pretty=format:%h|%cI|%an|%s",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    rows: list[tuple[str, str, str, str]] = []
    for line in out.splitlines():
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue
        sha, when, author, subject = parts
        # normalize date to UTC Z when possible
        when = when.strip()
        if when.endswith("+01:00") or re.search(r"[+-]\d{2}:\d{2}$", when):
            try:
                dt = datetime.fromisoformat(when)
                when = dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                pass
        elif when.endswith("Z"):
            pass
        subject = subject.replace("|", "\\|")
        rows.append((sha.strip(), when, author.strip(), subject.strip()))
    return rows


def render_changelog_block(
    commits: list[tuple[str, str, str, str]], synced: str
) -> str:
    lines = [
        CHANGELOG_BEGIN,
        "## Changelog",
        "",
        f"_Last synced: {synced}_",
        "",
        "Recent commits on this board repository.",
        "",
    ]
    if not commits:
        lines.append("_No commits recorded yet._")
    else:
        lines.extend(
            [
                "| Date (UTC) | SHA | Author | Message |",
                "|------------|-----|--------|---------|",
            ]
        )
        for sha, when, author, subject in commits:
            # show date-only for readability when possible
            day = when[:10] if len(when) >= 10 else when
            lines.append(f"| {day} | `{sha}` | {author} | {subject} |")
    lines.extend(["", CHANGELOG_END])
    return "\n".join(lines)


def upsert_section(text: str, pattern: re.Pattern[str], block: str) -> str:
    if pattern.search(text):
        return pattern.sub(block, text, count=1)
    # Insert before contributors block when present; else append
    contrib = "<!-- taskmark:contributors:begin -->"
    if contrib in text:
        return text.replace(contrib, block + "\n\n" + contrib, 1)
    return text.rstrip() + "\n\n" + block + "\n"


def refresh_readme(
    board: Path,
    *,
    dry_run: bool = False,
    changelog_limit: int = 40,
) -> bool:
    ra = _load_recompute()
    readme = board / "README.md"
    if not readme.exists():
        if dry_run:
            return False
        readme.write_text("# Taskmark board\n\n", encoding="utf-8")

    now = datetime.now(timezone.utc)
    synced = ra.fmt_ts(now)
    items = ra.load_items(board)
    leaves = [i for i in items if i.fm.get("type") in {"task", "bug"}]
    total, complete = aggregate_counts(items)
    speed, week_count = ra.compute_current_speed_pts_per_week(leaves, now)
    open_rows = open_work_rows(items)
    commits = board_git_log(board, changelog_limit)

    status_block = render_status_block(total, complete, speed, week_count, synced)
    open_block = render_open_work_block(open_rows, synced)
    changelog_block = render_changelog_block(commits, synced)

    text = readme.read_text(encoding="utf-8")
    new_text = text
    new_text = upsert_section(new_text, SECTION_PATTERNS["status"], status_block)
    new_text = upsert_section(new_text, SECTION_PATTERNS["open"], open_block)
    new_text = upsert_section(new_text, SECTION_PATTERNS["changelog"], changelog_block)
    if not new_text.endswith("\n"):
        new_text += "\n"

    if new_text == text:
        return False
    if not dry_run:
        readme.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("board", type=Path, help="Taskmark board root")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--changelog-limit", type=int, default=40)
    args = ap.parse_args()
    board = args.board.resolve()
    if not board.is_dir():
        print(f"Not a directory: {board}", file=sys.stderr)
        return 1
    changed = refresh_readme(
        board, dry_run=args.dry_run, changelog_limit=args.changelog_limit
    )
    state = "would update" if args.dry_run and changed else (
        "updated" if changed else "unchanged"
    )
    print(f"readme dashboard: {state} ({board / 'README.md'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
