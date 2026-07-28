---
name: new-epic
description: Create a new Taskmark epic on the project board
---

# New epic

Follow the `create-epic` skill. Gather title and goal from the user if missing, create the epic under `taskmark/epics/`, suggest t-shirt size, and update `INDEX.md`.

If the board does not exist yet, run **full** `taskmark-init` first (includes `ensure-board-ui.py` — Vercel Node `server.js` + `vercel.json`).
