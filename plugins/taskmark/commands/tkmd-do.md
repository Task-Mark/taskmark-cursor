---
description: Implement Taskmark work without committing
---

Use the `tkmd-do` skill to implement the requested target.

This command never commits or pushes and never touches any board file. The
board item is the spec; the Taskmark GitHub / Bitbucket App reconciles status,
logs, and commits after the work is pushed and merged.

Before changing code, work on a branch whose name contains the target id
(create `<id>-<short-slug>` from the current branch when needed).

When the target is a story or epic, every open, non-cancelled, non-shelved
descendant leaf is mandatory scope. If a definitive blocker prevents one leaf,
report the whole target incomplete.

Follow-up on a done item: just implement. Do not log anything on the item.
