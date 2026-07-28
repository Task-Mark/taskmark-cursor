---
name: new-task
description: Create a new Taskmark task or bug (story optional; may attach under epic)
---

# New task

Follow the `create-task` skill. Prefer a parent story when named or clear from context; otherwise attach under a named/inferred **epic**’s `items/` (no story). If neither fits, use **General** epic `items/`. Calibrate size from history, link from the parent, and sync status/INDEX.

If the board does not exist yet, run **full** `taskmark-init` first (includes Vercel Node stubs via `ensure-board-ui.py`).
