---
description: Implement Taskmark work without committing
---

Use the `tkmd-do` skill to implement the requested target.

This command never commits or pushes. It never introduces an `in_progress`
stage. Before stopping, mark every executed leaf done in that leaf file only.

If the request fits a done task, log Prompt & feedback there instead of
creating a duplicate. Create a new leaf only when nothing fits.
