#!/usr/bin/env python3
"""Print a collision-resistant Taskmark ID without modifying the board."""

from __future__ import annotations

import argparse
import json
import re
import secrets
import subprocess
from pathlib import Path

VALID_PREFIXES = {"E", "S", "T", "B"}


def git_name(cwd: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "config", "--get", "user.name"],
            cwd=cwd,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def identity_token(name: str) -> str:
    parts = re.findall(r"[A-Za-z0-9]+", name)
    if not parts:
        return "ANON"
    token = parts[0][:2] if len(parts) == 1 else parts[0][0] + parts[-1][0]
    token = re.sub(r"[^A-Za-z0-9]", "", token).upper()
    return token[:12] or "ANON"


def existing_ids(board: Path) -> set[str]:
    ids: set[str] = set()
    if not board.exists():
        return ids
    pattern = re.compile(r"^id:\s*[\"']?([^\"'\s]+)", re.MULTILINE)
    for path in board.rglob("*.md"):
        match = pattern.search(path.read_text(encoding="utf-8", errors="ignore"))
        if match:
            ids.add(match.group(1))
    return ids


def allocate(prefix: str, board: Path, identity: str) -> str:
    used = existing_ids(board)
    for _ in range(100):
        candidate = f"{prefix}-{identity}-{secrets.token_hex(4)}"
        if candidate not in used and not any(
            candidate in str(path) for path in board.glob("**/*")
        ):
            return candidate
    raise RuntimeError("could not allocate a unique ID after 100 attempts")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefix", choices=sorted(VALID_PREFIXES))
    parser.add_argument("board_root", type=Path)
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--identity", help="Identity token override")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    raw_identity = args.identity or identity_token(git_name(args.cwd))
    identity = re.sub(r"[^A-Za-z0-9]", "", raw_identity).upper()[:12] or "ANON"
    item_id = allocate(args.prefix, args.board_root.resolve(), identity)
    if args.json:
        print(json.dumps({"id": item_id, "identity": identity}))
    else:
        print(item_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
