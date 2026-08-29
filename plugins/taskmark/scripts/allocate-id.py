#!/usr/bin/env python3
"""Print a collision-resistant Taskmark ID without modifying the board."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import secrets
import subprocess
from pathlib import Path

VALID_PREFIXES = {"E", "S", "T", "B"}


def _load_identity_token():
    spec = importlib.util.spec_from_file_location(
        "taskmark_git_identity",
        Path(__file__).resolve().parent / "git-identity.py",
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load git-identity.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.identity_token


identity_token = _load_identity_token()


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
