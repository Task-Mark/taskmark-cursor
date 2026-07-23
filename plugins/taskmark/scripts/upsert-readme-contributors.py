#!/usr/bin/env python3
"""Upsert a managed Contributors section in project README(s)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BEGIN = "<!-- taskmark:contributors:begin -->"
END = "<!-- taskmark:contributors:end -->"

SECTION_RE = re.compile(
    re.escape(BEGIN) + r"[\s\S]*?" + re.escape(END),
    re.MULTILINE,
)


def normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def merge_people(
    existing: list[dict], incoming: list[dict]
) -> list[dict]:
    by_email: dict[str, dict] = {}
    order: list[str] = []
    for person in existing + incoming:
        name = str(person.get("name") or "").strip()
        email = str(person.get("email") or "").strip()
        initials = str(person.get("initials") or "").strip()
        key = normalize_email(email) or f"name:{(name or '').lower()}"
        if key in by_email:
            cur = by_email[key]
            if not cur.get("name") and name:
                cur["name"] = name
            if not cur.get("email") and email:
                cur["email"] = email
            if not cur.get("initials") and initials:
                cur["initials"] = initials
        else:
            by_email[key] = {"name": name, "email": email, "initials": initials}
            order.append(key)
    return [by_email[k] for k in order]


def parse_existing_block(text: str) -> list[dict]:
    m = SECTION_RE.search(text)
    if not m:
        return []
    block = m.group(0)
    people: list[dict] = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        # - Name <email> or - Name
        body = line[2:].strip()
        email_m = re.search(r"<([^>]+)>", body)
        email = email_m.group(1).strip() if email_m else ""
        name = re.sub(r"<[^>]+>", "", body).strip()
        if name or email:
            people.append({"name": name, "email": email, "initials": ""})
    return people


def render_block(people: list[dict]) -> str:
    lines = [
        BEGIN,
        "## Contributors",
        "",
        "People who created or resolved work items on this board (from local git config).",
        "",
    ]
    if not people:
        lines.append("_No contributors recorded yet._")
    else:
        for p in people:
            name = p.get("name") or "Unknown"
            email = p.get("email") or ""
            if email:
                lines.append(f"- {name} <{email}>")
            else:
                lines.append(f"- {name}")
    lines.extend(["", END])
    return "\n".join(lines)


def upsert_readme(path: Path, people: list[dict]) -> bool:
    if not path.exists():
        path.write_text("# Project\n\n", encoding="utf-8")
    text = path.read_text(encoding="utf-8")
    existing = parse_existing_block(text)
    merged = merge_people(existing, people)
    block = render_block(merged)
    if SECTION_RE.search(text):
        new_text = SECTION_RE.sub(block, text, count=1)
    else:
        new_text = text.rstrip() + "\n\n" + block + "\n"
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "readme",
        nargs="+",
        type=Path,
        help="README.md path(s) to update",
    )
    parser.add_argument(
        "--people-json",
        required=True,
        help='JSON array of {"name","email","initials"}',
    )
    args = parser.parse_args()
    try:
        people = json.loads(args.people_json)
        if not isinstance(people, list):
            people = []
    except json.JSONDecodeError:
        print("Invalid --people-json", file=sys.stderr)
        return 1
    changed = False
    for path in args.readme:
        if upsert_readme(path, people):
            print(f"updated: {path}")
            changed = True
        else:
            print(f"unchanged: {path}")
    return 0 if changed or True else 0


if __name__ == "__main__":
    sys.exit(main())
