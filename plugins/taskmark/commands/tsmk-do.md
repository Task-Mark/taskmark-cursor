---
description: Implement Taskmark work without committing
---

Use the `tsmk-do` skill to implement the requested target.

This command never commits or pushes. It never introduces an `in_progress`
stage. Before stopping, mark every executed leaf done in that leaf file only.
