---
description: Implement Taskmark work without committing
---

Use the `tkmd-do` skill to implement the requested target.

This command never commits or pushes. It never introduces an `in_progress`
stage. Before stopping, mark every executed leaf done in that leaf file only.

When the target is a story or epic, every open, non-cancelled descendant leaf
is mandatory scope. Do not stop successfully until all descendants are done;
their parent statuses are derived at read time and parent markdown stays
unchanged. If a definitive blocker prevents one leaf from completing, leave it
open and report the whole target incomplete.

If the request fits a done task, log Prompt & feedback there instead of
creating a duplicate. Create a new leaf only when nothing fits.
