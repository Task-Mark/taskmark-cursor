---
description: Save a Cursor Plan mode plan as Taskmark work items
---

Use the `tkmd-save` skill.

Read the Cursor Plan mode plan from this session or from a path the user
points at. Search the canonical board, including request briefs, avoid
duplicates, and create the smallest useful hierarchy of new files, including
diagrams and other visuals from the plan, in the board writing language.

On a request board (`requests/` exists), place the new items under
`requests/<slug>/epics/...` of the request the plan fits, or create a new
request with `requests/<slug>/brief.md` when it is a new need. Never edit an
existing brief. On a legacy board (`epics/` and no `requests/`), keep writing
under `epics/` and suggest `npx taskmark init` to migrate.

Do not implement work. Never commit, push, or use `in_progress`.
