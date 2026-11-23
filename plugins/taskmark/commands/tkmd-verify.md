---
description: Migrate an existing board to the current Taskmark layout
---

Use the `tkmd-verify` skill.

Locate the canonical board, repair the scaffold like `/tkmd-init`, delete
leftover generated files, and strip legacy item markdown (retired
frontmatter and parent child lists only). This maintainer-only migration is
the only command that rewrites existing item files; it never touches status,
dates, resolvers, criteria, or log and commit rows. Never commit or push.
Never create `INDEX.md`, `SIZING.md`, `VELOCITY.md`, or `CHANGELOG.md`.
When the user asks not to write yet, pass `--dry-run` to `verify-board.py`.
