---
description: Plan Taskmark work from prose
---

Use the `tkmd-plan` skill. Search the canonical board, including request
briefs, avoid duplicate or overlapping work, and plan the smallest useful
hierarchy from the user's prose.

On a request board (`requests/` exists), add the new epics, stories, and tasks
under `requests/<slug>/epics/...` of the request the work fits, or create a
new request with `requests/<slug>/brief.md` when it is a new need. On a legacy
board (`epics/` and no `requests/`), keep writing under `epics/` and suggest
`npx taskmark init` to migrate.

Write new item files only, in the board writing language. Never rewrite an
existing parent, an existing request brief, or any derived board file.
