---
description: Shelve Taskmark work that will not be implemented
---

Use the `tkmd-shelf` skill to discard the requested target.

This command never commits or pushes. It marks eligible task/bug leaves
`status: shelved` with `completed_at` set, without checking acceptance criteria
or claiming the work was implemented.

For a story or epic, shelve every open, non-cancelled, non-shelved descendant
leaf. Parent markdown remains unchanged because parent status is derived at
read time.
