---
description: Save a Cursor Plan mode plan as Taskmark items, then implement them
---

Use the `tkmd-save-do` skill.

This command never commits or pushes. It never introduces an `in_progress`
stage. Save first like `/tkmd-save`, under an existing or new request on a
request board. If save created new item files, implement only that new work
like `/tkmd-do`, without editing the new items afterwards. If save created
nothing, report the matching item and skip implementation.
