#!/usr/bin/env python3
"""Ensure the reserved General epic exists on a board (with epic-level items/).

Usage:
  ensure-general-epic.py <board-root>

Prints JSON: {"epic_id","epic_path","items_dir","created_epic"}

Identification (any match):
  - epic title equals "General" (case-insensitive)
  - folder slug is "{id}-general"
  - tags include "general"

General tasks/bugs attach under epics/{E-NNN}-general/items/ (no story).
Do not create an Unattached catch-all story.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

FM_RE = re.compile(r"^---\r?\n(.*?)\r?\n---", re.DOTALL | re.MULTILINE)
ID_RE = re.compile(r"^id:\s*(E-\d+|S-\d+)", re.MULTILINE)
TITLE_RE = re.compile(r"^title:\s*(.+)$", re.MULTILINE)
TAGS_RE = re.compile(r"^tags:\s*\[(.*?)\]", re.MULTILINE)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def parse_frontmatter(text: str) -> dict[str, str]:
    m = FM_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    out: dict[str, str] = {}
    id_m = ID_RE.search(block)
    if id_m:
        out["id"] = id_m.group(1)
    title_m = TITLE_RE.search(block)
    if title_m:
        out["title"] = title_m.group(1).strip().strip('"').strip("'")
    tags_m = TAGS_RE.search(block)
    if tags_m:
        raw = tags_m.group(1).strip()
        out["tags"] = raw
    return out


def tags_list(raw: str) -> list[str]:
    if not raw:
        return []
    return [t.strip().strip('"').strip("'") for t in raw.split(",") if t.strip()]


def next_id(board: Path, prefix: str) -> str:
    nums: list[int] = []
    for path in board.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        m = re.search(rf"^id:\s*{prefix}-(\d+)", text, re.MULTILINE)
        if m:
            nums.append(int(m.group(1)))
    n = max(nums) + 1 if nums else 1
    return f"{prefix}-{n:03d}"


def find_general_epic(epics_dir: Path) -> tuple[Path, str] | None:
    if not epics_dir.is_dir():
        return None
    for entry in sorted(epics_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        epic_md = entry / "epic.md"
        if not epic_md.is_file():
            continue
        fm = parse_frontmatter(epic_md.read_text(encoding="utf-8"))
        eid = fm.get("id", "")
        title = fm.get("title", "")
        tags = tags_list(fm.get("tags", ""))
        slug_general = entry.name.endswith("-general") or entry.name == "general"
        if title.lower() == "general" or "general" in tags or slug_general:
            return epic_md, eid or entry.name.split("-")[0]
    return None


def write_general_epic(path: Path, eid: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    (path.parent / "items").mkdir(exist_ok=True)
    (path.parent / "stories").mkdir(exist_ok=True)
    ts = now_iso()
    path.write_text(
        f"""---
id: {eid}
type: epic
title: General
status: backlog
priority: medium
size: null
size_source: rolled_up
size_basis: [sum:children]
points: 0
points_source: rolled_up
estimate_minutes: 0
actual_minutes: 0
estimate_source: rolled_up
estimate_basis: [sum:children]
session_cap_minutes: 480
parent: null
epic: null
owner: ""
blocked: false
cancelled: false
tags: [general]
created: {today()}
updated: {ts}
started_at: null
completed_at: null
---

# {eid}: General

## Goal

Default home for general tasks and user stories that do not have a clearer epic.

## Scope

- General user stories created without an explicit epic.
- General tasks/bugs without an explicit story (`items/` under this epic).

## Out of scope

- Product initiatives that deserve their own epic (move them out of General when known).

## Success metrics

- General tasks and user stories remain visible in the epic list under General.

## Stories

## Commits

| SHA | Repo | Date (UTC) | Message |
|-----|------|------------|---------|

## Work log

| Session | Actor | Started (UTC) | Ended (UTC) | Summary |
|---------|-------|---------------|-------------|---------|
""",
        encoding="utf-8",
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: ensure-general-epic.py <board-root>", file=sys.stderr)
        return 2
    board = Path(sys.argv[1]).resolve()
    if not board.is_dir():
        print(f"Not a directory: {board}", file=sys.stderr)
        return 1

    epics_dir = board / "epics"
    epics_dir.mkdir(parents=True, exist_ok=True)

    created_epic = False
    found = find_general_epic(epics_dir)
    if found:
        epic_md, eid = found
    else:
        eid = next_id(board, "E")
        epic_md = epics_dir / f"{eid}-general" / "epic.md"
        write_general_epic(epic_md, eid)
        created_epic = True

    items_dir = epic_md.parent / "items"
    items_dir.mkdir(parents=True, exist_ok=True)
    (epic_md.parent / "stories").mkdir(parents=True, exist_ok=True)

    result = {
        "epic_id": eid,
        "epic_path": str(epic_md),
        "items_dir": str(items_dir),
        "created_epic": created_epic,
    }
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
