#!/usr/bin/env python3
"""Migrate an existing Taskmark board to the current layout.

Deletes leftover generated files at the canonical board root and strips
retired frontmatter / parent-only sections from item markdown. Does not
commit, push, create INDEX/SIZING/VELOCITY/CHANGELOG, or rewrite IDs.

Usage:
  python3 verify-board.py <board-root> [--dry-run] [--workspace PATH ...]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

RETIRED_FRONTMATTER = {
    "owner",
    "estimate_minutes",
    "estimate_source",
    "estimate_basis",
    "actual_minutes",
    "actual_ms",
    "size_source",
    "size_basis",
    "points_source",
    "session_cap_minutes",
}

FORBIDDEN_GENERATED = {"INDEX.md", "SIZING.md", "VELOCITY.md"}
ID_COUNTER_NAMES = {
    "NEXT_IDS",
    "NEXT_IDS.md",
    "NEXT_IDS.txt",
    "NEXT_IDS.json",
    "next_ids",
    "next_ids.md",
}
PARENT_DROP_HEADINGS = {
    "stories",
    "tasks",
    "bugs",
    "items",
    "children",
    "work items",
    "child list",
    "prompt & feedback",
    "commits",
    "work log",
}
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
KEY_RE = re.compile(r"^([A-Za-z0-9_]+)\s*:")
KEEP_NAMES = {"CHANGELOG.md", "epics", "node_modules", "out"}


def is_generated_dashboard(text: str) -> bool:
    if "Last synced" in text or "Current speed" in text:
        return True
    lowered = text.lower()
    if "readme changelog" in lowered:
        return True
    if "open-work" in lowered or "## open work" in lowered:
        return True
    return False


def indent_width(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def strip_retired_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    parts = text.split("\n")
    if parts[0].strip() != "---":
        return text
    end = None
    for i in range(1, len(parts)):
        if parts[i].strip() == "---":
            end = i
            break
    if end is None:
        return text
    kept: list[str] = [parts[0]]
    skip_indent: int | None = None
    for line in parts[1:end]:
        if skip_indent is not None:
            if line.strip() == "":
                continue
            if indent_width(line) > skip_indent and not KEY_RE.match(line):
                continue
            skip_indent = None
        match = KEY_RE.match(line)
        if match and match.group(1) in RETIRED_FRONTMATTER:
            skip_indent = indent_width(line)
            continue
        kept.append(line)
    kept.append(parts[end])
    kept.extend(parts[end + 1 :])
    return "\n".join(kept)


def heading_key(title: str) -> str:
    cleaned = re.sub(r"[*_`]", "", title).strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def strip_parent_sections(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        match = HEADING_RE.match(lines[i])
        if match:
            level = len(match.group(1))
            key = heading_key(match.group(2))
            if key in PARENT_DROP_HEADINGS:
                i += 1
                while i < len(lines):
                    nxt = HEADING_RE.match(lines[i])
                    if nxt and len(nxt.group(1)) <= level:
                        break
                    i += 1
                while out and out[-1].strip() == "":
                    out.pop()
                if i < len(lines):
                    out.append("")
                continue
        out.append(lines[i])
        i += 1
    result = "\n".join(out)
    if text.endswith("\n") and not result.endswith("\n"):
        result += "\n"
    return result


def migrate_markdown(path: Path, dry_run: bool) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = strip_retired_frontmatter(original)
    if path.name in {"epic.md", "story.md"}:
        updated = strip_parent_sections(updated)
    if updated == original:
        return False
    if not dry_run:
        path.write_text(updated, encoding="utf-8")
    return True


def delete_if_present(path: Path, dry_run: bool) -> bool:
    if not path.exists():
        return False
    if not dry_run:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    return True


def looks_like_generated_duplicate(folder: Path) -> bool:
    if not folder.is_dir():
        return False
    names = {p.name for p in folder.iterdir() if p.name != ".DS_Store"}
    if "epics" in names:
        epics = folder / "epics"
        has_items = any(epics.rglob("*.md")) if epics.is_dir() else False
        if has_items:
            return False
    allowed = FORBIDDEN_GENERATED | ID_COUNTER_NAMES | {"README.md", "epics"}
    return names <= allowed


def static_readme_path(board: Path) -> Path:
    if board.name == "taskmark":
        return board.parent / "README.md"
    return board / "README.md"


def nested_dashboard_readme(board: Path) -> Path | None:
    if board.name == "taskmark":
        nested = board / "README.md"
    else:
        nested = board / "taskmark" / "README.md"
    if nested.is_file():
        return nested
    return None


def find_extra_taskmark_dirs(board: Path, workspaces: list[Path]) -> list[Path]:
    extras: list[Path] = []
    seen = {board.resolve()}
    roots = workspaces or [board.parent, board]
    for base in roots:
        if not base.exists():
            continue
        for candidate in base.rglob("taskmark"):
            if not candidate.is_dir():
                continue
            resolved = candidate.resolve()
            if resolved in seen:
                continue
            if resolved == board.resolve():
                continue
            if "node_modules" in resolved.parts:
                continue
            seen.add(resolved)
            extras.append(resolved)
    return extras


def verify(board: Path, dry_run: bool, workspaces: list[Path]) -> dict:
    board = board.resolve()
    deleted: list[str] = []
    rewritten: list[str] = []
    reported: list[str] = []

    for name in FORBIDDEN_GENERATED:
        path = board / name
        if delete_if_present(path, dry_run):
            deleted.append(str(path))

    for entry in board.iterdir():
        if entry.name in ID_COUNTER_NAMES or entry.name.upper() in {
            n.upper() for n in ID_COUNTER_NAMES
        }:
            if entry.name in KEEP_NAMES:
                continue
            if delete_if_present(entry, dry_run):
                deleted.append(str(entry))

    static_readme = static_readme_path(board)
    static_ok = static_readme.is_file() and not is_generated_dashboard(
        static_readme.read_text(encoding="utf-8")
    )
    nested = nested_dashboard_readme(board)
    if nested and static_ok:
        text = nested.read_text(encoding="utf-8")
        if is_generated_dashboard(text):
            if delete_if_present(nested, dry_run):
                deleted.append(str(nested))

    epics = board / "epics"
    if epics.is_dir():
        for md in sorted(epics.rglob("*.md")):
            if migrate_markdown(md, dry_run):
                rewritten.append(str(md.relative_to(board)))

    for extra in find_extra_taskmark_dirs(board, workspaces):
        if looks_like_generated_duplicate(extra):
            if delete_if_present(extra, dry_run):
                deleted.append(str(extra))
        else:
            reported.append(str(extra))

    return {
        "board": str(board),
        "dry_run": dry_run,
        "deleted": deleted,
        "rewritten": rewritten,
        "rewritten_count": len(rewritten),
        "reported_extra_taskmark": reported,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("board_root", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--workspace",
        action="append",
        default=[],
        type=Path,
        help="Workspace roots used to find extra taskmark/ copies",
    )
    args = ap.parse_args()
    board = args.board_root.resolve()
    if not board.is_dir():
        print(f"error: not a directory: {board}", file=sys.stderr)
        return 1
    report = verify(board, args.dry_run, list(args.workspace))
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
