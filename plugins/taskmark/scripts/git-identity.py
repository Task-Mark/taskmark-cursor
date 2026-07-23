#!/usr/bin/env python3
"""Git identity helpers for Taskmark: read git config, initials, merge lists."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def git_config(key: str, cwd: Path | None = None) -> str:
    cmd = ["git", "config", "--get", key]
    try:
        out = subprocess.check_output(
            cmd,
            cwd=str(cwd) if cwd else None,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return ""


def derive_initials(name: str) -> str:
    parts = [p for p in re.split(r"[\s\-_.]+", (name or "").strip()) if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        token = parts[0]
        return (token[:2] if len(token) >= 2 else token[:1]).upper()
    return (parts[0][0] + parts[-1][0]).upper()


def read_git_identity(cwd: Path | None = None) -> dict[str, str] | None:
    """Return {name, email, initials} from local then global git config, or None."""
    name = git_config("user.name", cwd) or git_config("user.name", None)
    email = git_config("user.email", cwd) or git_config("user.email", None)
    if not name and not email:
        return None
    name = name or email.split("@")[0]
    email = email or ""
    return {
        "name": name,
        "email": email,
        "initials": derive_initials(name),
    }


def normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def merge_identity(
    existing: list[dict[str, Any]], identity: dict[str, str] | None
) -> list[dict[str, Any]]:
    """Append identity by email (case-insensitive); fill missing name/initials."""
    if not identity:
        return list(existing)
    email_key = normalize_email(identity.get("email", ""))
    name = (identity.get("name") or "").strip()
    initials = (identity.get("initials") or derive_initials(name)).strip()
    out: list[dict[str, Any]] = []
    found = False
    for item in existing:
        if not isinstance(item, dict):
            continue
        cur = {
            "name": str(item.get("name") or "").strip(),
            "email": str(item.get("email") or "").strip(),
            "initials": str(item.get("initials") or "").strip(),
        }
        if email_key and normalize_email(cur["email"]) == email_key:
            found = True
            if not cur["name"] and name:
                cur["name"] = name
            if not cur["initials"]:
                cur["initials"] = initials or derive_initials(cur["name"])
            if email_key and not cur["email"]:
                cur["email"] = identity.get("email", "")
        elif not email_key and name and cur["name"].lower() == name.lower():
            found = True
            if not cur["email"] and identity.get("email"):
                cur["email"] = identity["email"]
            if not cur["initials"]:
                cur["initials"] = initials or derive_initials(cur["name"])
        if not cur["initials"] and cur["name"]:
            cur["initials"] = derive_initials(cur["name"])
        out.append(cur)
    if not found:
        out.append(
            {
                "name": name,
                "email": identity.get("email", ""),
                "initials": initials or derive_initials(name),
            }
        )
    return out


def identity_to_yaml_list(identities: list[dict[str, Any]]) -> str:
    if not identities:
        return "[]"
    lines = [""]
    for ident in identities:
        lines.append(f"  - name: {json.dumps(ident.get('name') or '', ensure_ascii=False)}")
        lines.append(f"    email: {json.dumps(ident.get('email') or '', ensure_ascii=False)}")
        lines.append(
            f"    initials: {json.dumps(ident.get('initials') or '', ensure_ascii=False)}"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read or merge git identity")
    parser.add_argument(
        "--cwd",
        type=Path,
        default=None,
        help="Git repo directory for local config",
    )
    parser.add_argument(
        "--merge-json",
        default=None,
        help="JSON array of existing identities to merge current git user into",
    )
    parser.add_argument(
        "--format",
        choices=("json", "yaml-list"),
        default="json",
    )
    args = parser.parse_args()
    ident = read_git_identity(args.cwd)
    if args.merge_json is not None:
        try:
            existing = json.loads(args.merge_json)
            if not isinstance(existing, list):
                existing = []
        except json.JSONDecodeError:
            existing = []
        merged = merge_identity(existing, ident)
        if args.format == "yaml-list":
            print(identity_to_yaml_list(merged))
        else:
            print(json.dumps(merged, ensure_ascii=False))
        return 0
    if ident is None:
        if args.format == "yaml-list":
            print("[]")
        else:
            print("null")
        return 0
    if args.format == "yaml-list":
        print(identity_to_yaml_list([ident]))
    else:
        print(json.dumps(ident, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
