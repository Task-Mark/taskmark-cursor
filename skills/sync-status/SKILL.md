---
name: sync-status
description: >-
  Recompute derived Taskmark status and size rollups for an item and its ancestors,
  then refresh taskmark/INDEX.md. Use after acceptance-criteria edits, work-log
  changes, creating children, or when the user asks to sync or recalculate board
  status.
---

# sync-status

## Prerequisites

- Read [status-derivation](../taskmark-conventions/references/status-derivation.md), [sizing](../taskmark-conventions/references/sizing.md), [index-format](../taskmark-conventions/references/index-format.md).

## Steps

1. Resolve starting item (id/path) or sync the **entire board** if the user asks for a full sync / board refresh.
2. For each task/bug in scope: derive `status` from latches, AC checkboxes, open sessions, `started_at`; set `completed_at` when entering `done`.
3. For each story: roll up child item statuses; recompute `size` from child weights; bump `updated` if changed.
4. For each epic: roll up child stories; recompute `size`; bump `updated` if changed.
5. Rewrite `taskmark/INDEX.md` completely from current frontmatter (all epics, stories, items, open sessions).
6. Report what changed (ids + old → new status/size).

## Full board sync

Scan `taskmark/epics/**/*.md`, process leaves (items) first, then stories, then epics, then INDEX.
