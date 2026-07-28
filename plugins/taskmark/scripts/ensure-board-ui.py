#!/usr/bin/env python3
"""Ensure a Taskmark board root has UI + Vercel Node deploy stubs.

Idempotent. Used by taskmark-init and any skill that bootstraps a board.

Copies / merges from examples/board-ui-stub/:
  - package.json  (name, @taskmark/ui dep, start/serve scripts, type:module)
  - server.js     (Vercel Framework Preset: Node entry)
  - vercel.json   (framework: node)

Usage:
  python3 ensure-board-ui.py <board-root> [--name <package-name>] [--force]
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


def stub_dir() -> Path:
    # scripts/ → plugin root → examples/board-ui-stub
    return Path(__file__).resolve().parent.parent / "examples" / "board-ui-stub"


def ensure_gitignore(board: Path) -> bool:
    gi = board / ".gitignore"
    line = "node_modules/"
    if gi.exists():
        text = gi.read_text(encoding="utf-8")
        if "node_modules" in text:
            return False
        if text and not text.endswith("\n"):
            text += "\n"
        gi.write_text(text + line + "\n", encoding="utf-8")
        return True
    gi.write_text(line + "\n", encoding="utf-8")
    return True


def merge_package_json(board: Path, stub: Path, package_name: str | None, force: bool) -> str:
    stub_pkg = json.loads((stub / "package.json").read_text(encoding="utf-8"))
    pkg_path = board / "package.json"
    created = False
    if pkg_path.exists() and not force:
        pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
        action = "updated"
    else:
        pkg = dict(stub_pkg)
        created = True
        action = "created"

    if package_name:
        pkg["name"] = package_name
    elif created and not pkg.get("name"):
        pkg["name"] = board.name

    pkg["private"] = True
    pkg["type"] = "module"
    pkg.setdefault("engines", stub_pkg.get("engines", {"node": ">=18"}))
    if "description" not in pkg or created:
        pkg["description"] = stub_pkg.get(
            "description",
            "Taskmark board — npm start / taskmark serve; Vercel Node via server.js.",
        )

    scripts = pkg.setdefault("scripts", {})
    scripts.setdefault("start", "taskmark serve --no-open")
    scripts.setdefault("serve", "taskmark serve")
    scripts.setdefault("dev", "taskmark serve")

    deps = pkg.setdefault("dependencies", {})
    # Always production dep — Vercel omits devDependencies on install.
    # Migrate any legacy --save-dev / -D install into dependencies.
    dev = dict(pkg.get("devDependencies") or {})
    if "@taskmark/ui" in dev:
        ver = deps.get("@taskmark/ui") or dev["@taskmark/ui"]
        del dev["@taskmark/ui"]
        deps["@taskmark/ui"] = ver
        if not dev:
            pkg.pop("devDependencies", None)
        else:
            pkg["devDependencies"] = dev
    deps.setdefault(
        "@taskmark/ui",
        stub_pkg.get("dependencies", {}).get("@taskmark/ui", "^0.1.0"),
    )

    pkg_path.write_text(json.dumps(pkg, indent=2) + "\n", encoding="utf-8")
    return action


def copy_if_needed(board: Path, stub: Path, name: str, force: bool) -> str:
    src = stub / name
    dest = board / name
    if not src.exists():
        return f"missing-stub:{name}"
    if dest.exists() and not force:
        return "skipped"
    existed = dest.exists()
    shutil.copy2(src, dest)
    return "overwritten" if existed else "copied"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("board_root", type=Path, help="Board root (INDEX.md / epics)")
    ap.add_argument("--name", default=None, help="package.json name override")
    ap.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing server.js / vercel.json / package.json from stub",
    )
    args = ap.parse_args()
    board = args.board_root.resolve()
    if not board.is_dir():
        print(f"error: not a directory: {board}", file=sys.stderr)
        return 1

    stub = stub_dir()
    if not stub.is_dir():
        print(f"error: stub not found: {stub}", file=sys.stderr)
        return 1

    board.mkdir(parents=True, exist_ok=True)
    gi = ensure_gitignore(board)
    pkg_action = merge_package_json(board, stub, args.name, args.force)
    server_action = copy_if_needed(board, stub, "server.js", args.force)
    vercel_action = copy_if_needed(board, stub, "vercel.json", args.force)

    print(
        json.dumps(
            {
                "board": str(board),
                "gitignore_node_modules": gi,
                "package_json": pkg_action,
                "server_js": server_action,
                "vercel_json": vercel_action,
                "stub": str(stub),
            },
            indent=2,
        )
    )
    print(
        "Vercel Node stub ready — Framework Preset: Node (server.js). "
        "Next: npm install @taskmark/ui --save && npx taskmark serve",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
