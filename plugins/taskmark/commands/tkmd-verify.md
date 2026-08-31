---
description: Migrate an existing board to the current Taskmark layout
---

Use the `tkmd-verify` skill.

Locate the canonical board, repair the scaffold like `/tkmd-init`, delete
leftover generated files, and strip legacy item markdown. Never commit or
push. Never create `INDEX.md`, `SIZING.md`, `VELOCITY.md`, or `CHANGELOG.md`.
When the user asks not to write yet, pass `--dry-run` to `verify-board.py`.
