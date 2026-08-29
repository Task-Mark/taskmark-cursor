#!/usr/bin/env python3
"""Ensure a Taskmark board root has UI + Vercel Node deploy stubs.

Idempotent. Used by taskmark-init and any skill that bootstraps a board.

Copies / merges from examples/board-ui-stub/:
  - package.json  (name, @taskmark/ui dep, start/serve scripts, type:module)
  - server.js     (legacy Vercel Node entry; optional)
  - vercel.json   (static out/ hosting)
  - Dockerfile, compose.yaml, .dockerignore  (serve out/ on port 8275)

Usage:
  python3 ensure-board-ui.py <board-root> [--name <package-name>] [--force]
    [--writing-language <lang>] [--replace-writing-language]
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
    lines = ["REPOS.md", "node_modules/", "out/", ".taskmark-ui-build/"]
    changed = False
    if gi.exists():
        text = gi.read_text(encoding="utf-8")
        for line in lines:
            if line.rstrip("/") not in text and line not in text:
                if text and not text.endswith("\n"):
                    text += "\n"
                text += line + "\n"
                changed = True
        if changed:
            gi.write_text(text, encoding="utf-8")
        return changed
    gi.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def apply_writing_language(
    pkg: dict,
    writing_language: str | None,
    replace: bool,
) -> None:
    """Merge taskmark.writingLanguage without clobbering other package.json keys.

    An existing value is kept unless --replace-writing-language is set.
    A missing value is filled only when --writing-language is passed.
    """
    lang = (writing_language or "").strip()
    tm = pkg.get("taskmark")
    if not isinstance(tm, dict):
        tm = {}
    existing = tm.get("writingLanguage")
    if isinstance(existing, str):
        existing = existing.strip() or None
    else:
        existing = None
    if existing and not replace:
        if tm:
            pkg["taskmark"] = tm
        return
    if not lang:
        if tm:
            pkg["taskmark"] = tm
        return
    tm["writingLanguage"] = lang
    pkg["taskmark"] = tm


def merge_package_json(
    board: Path,
    stub: Path,
    package_name: str | None,
    force: bool,
    writing_language: str | None = None,
    replace_writing_language: bool = False,
) -> str:
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
    pkg.setdefault("version", stub_pkg.get("version", "0.1.0"))
    pkg.setdefault("engines", stub_pkg.get("engines", {"node": ">=18"}))
    if "description" not in pkg or created:
        pkg["description"] = stub_pkg.get(
            "description",
            "Taskmark board — npm start / taskmark serve; Vercel static via npm run build.",
        )

    scripts = pkg.setdefault("scripts", {})
    scripts.setdefault("start", "taskmark serve --no-open")
    scripts.setdefault("serve", "taskmark serve")
    scripts["dev"] = stub_pkg.get("scripts", {}).get("dev", "taskmark dev")
    scripts.setdefault("preview", "taskmark preview")
    scripts["build"] = stub_pkg.get("scripts", {}).get(
        "build", "taskmark build --board . --out out"
    )
    if stub_pkg.get("scripts", {}).get("preview"):
        scripts["preview"] = stub_pkg["scripts"]["preview"]

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

    apply_writing_language(pkg, writing_language, replace_writing_language)

    pkg_path.write_text(
        json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
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
    ap.add_argument("board_root", type=Path, help="Board root containing epics/")
    ap.add_argument("--name", default=None, help="package.json name override")
    ap.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing server.js / vercel.json / package.json from stub",
    )
    ap.add_argument(
        "--writing-language",
        default=None,
        help="Board writing language (any language). Fills a missing field; "
        "does not overwrite an existing value unless --replace-writing-language.",
    )
    ap.add_argument(
        "--replace-writing-language",
        action="store_true",
        help="Overwrite taskmark.writingLanguage (user explicitly changed it)",
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
    pkg_action = merge_package_json(
        board,
        stub,
        args.name,
        args.force,
        args.writing_language,
        args.replace_writing_language,
    )
    server_action = copy_if_needed(board, stub, "server.js", args.force)
    vercel_action = copy_if_needed(board, stub, "vercel.json", args.force)
    # Always refresh vercel.json to static hosting when force, or when still Node-era.
    if vercel_action == "skipped":
        existing = (board / "vercel.json").read_text(encoding="utf-8")
        if '"framework": "node"' in existing or "server.js" in existing:
            shutil.copy2(stub / "vercel.json", board / "vercel.json")
            vercel_action = "migrated-static"

    docker_files = {
        name: copy_if_needed(board, stub, name, args.force)
        for name in ("Dockerfile", "compose.yaml", ".dockerignore")
    }

    print(
        json.dumps(
            {
                "board": str(board),
                "gitignore_updated": gi,
                "package_json": pkg_action,
                "server_js": server_action,
                "vercel_json": vercel_action,
                "dockerfile": docker_files.get("Dockerfile"),
                "compose_yaml": docker_files.get("compose.yaml"),
                "dockerignore": docker_files.get(".dockerignore"),
                "stub": str(stub),
            },
            indent=2,
        )
    )
    print(
        "Vercel static stub ready — npm run build → out/. "
        "Next: npm install @taskmark/ui --save && npx taskmark serve",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
