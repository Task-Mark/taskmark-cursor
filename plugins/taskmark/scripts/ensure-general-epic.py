#!/usr/bin/env python3
"""Ensure the reserved General epic (and Unattached catch-all story) exist on a board.

Usage:
  ensure-general-epic.py <board-root>

Prints JSON: {"epic_id","epic_path","story_id","story_path","created_epic","created_story"}

Identification (any match):
  - epic title equals "General" (case-insensitive)
  - folder slug is "{id}-general"
  - tags include "general"

Catch-all story under General:
  - title "Unattached" (case-insensitive), or slug "{id}-unattached", or tag "unattached"
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
        if (
            title.lower() == "general"
            or "general" in tags
            or slug_general
        ):
            return epic_md, eid or entry.name.split("-")[0]
    return None


def find_unattached_story(stories_dir: Path) -> tuple[Path, str] | None:
    if not stories_dir.is_dir():
        return None
    for entry in sorted(stories_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        story_md = entry / "story.md"
        if not story_md.is_file():
            continue
        fm = parse_frontmatter(story_md.read_text(encoding="utf-8"))
        sid = fm.get("id", "")
        title = fm.get("title", "")
        tags = tags_list(fm.get("tags", ""))
        slug_ok = entry.name.endswith("-unattached") or entry.name == "unattached"
        if title.lower() == "unattached" or "unattached" in tags or slug_ok:
            return story_md, sid or entry.name.split("-")[0]
    return None


def write_general_epic(path: Path, eid: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
size_basis: [sum:stories]
points: 0
points_source: rolled_up
estimate_minutes: 0
actual_minutes: 0
estimate_source: rolled_up
estimate_basis: [sum:stories]
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

Default home for stories and tasks that do not have a clearer epic.

## Scope

- Unattached stories created without an explicit epic.
- Catch-all story **Unattached** for tasks/bugs without an explicit story.

## Out of scope

- Product initiatives that deserve their own epic (move them out of General when known).

## Success metrics

- Unattached work remains visible in the epic list under General.

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


def write_unattached_story(path: Path, sid: str, eid: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    (path.parent / "items").mkdir(exist_ok=True)
    ts = now_iso()
    path.write_text(
        f"""---
id: {sid}
type: story
title: Unattached
status: backlog
priority: medium
size: XS
size_source: suggested
size_basis: [general:catch-all]
points: 0
points_source: rolled_up
estimate_minutes: 0
actual_minutes: 0
estimate_source: rolled_up
estimate_basis: [sum:tasks]
session_cap_minutes: 480
parent: {eid}
epic: {eid}
owner: ""
blocked: false
cancelled: false
tags: [unattached, general]
created: {today()}
updated: {ts}
started_at: null
completed_at: null
---

# {sid}: Unattached

## User story

As a user, I want a catch-all story under General so tasks without a named story still have a valid board path.

## Acceptance criteria

- [ ] Tasks/bugs without an explicit story can live under this story.
- [ ] Prefer moving work to a real story when one becomes clear.

## Tasks

## Prompt & feedback log

| # | When (UTC) | Kind | Summary |
|---|------------|------|---------|

## Commits

| SHA | Repo | Date (UTC) | Message |
|-----|------|------------|---------|

## Work log

| Session | Actor | Started (UTC) | Ended (UTC) | Summary |
|---------|-------|---------------|-------------|---------|
""",
        encoding="utf-8",
    )


def link_story_from_epic(epic_md: Path, sid: str, title: str, rel: str) -> None:
    text = epic_md.read_text(encoding="utf-8")
    marker = f"[{sid}:"
    if marker in text:
        return
    link = f"- [{sid}: {title}]({rel})\n"
    if "## Stories\n" in text:
        text = text.replace("## Stories\n", f"## Stories\n\n{link}", 1)
    else:
        text += f"\n## Stories\n\n{link}"
    epic_md.write_text(text, encoding="utf-8")


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

    stories_dir = epic_md.parent / "stories"
    stories_dir.mkdir(parents=True, exist_ok=True)

    created_story = False
    found_story = find_unattached_story(stories_dir)
    if found_story:
        story_md, sid = found_story
    else:
        sid = next_id(board, "S")
        story_md = stories_dir / f"{sid}-unattached" / "story.md"
        write_unattached_story(story_md, sid, eid)
        created_story = True
        rel = f"stories/{story_md.parent.name}/story.md"
        link_story_from_epic(epic_md, sid, "Unattached", rel)

    result = {
        "epic_id": eid,
        "epic_path": str(epic_md),
        "story_id": sid,
        "story_path": str(story_md),
        "created_epic": created_epic,
        "created_story": created_story,
    }
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
