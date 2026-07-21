---
name: create-task
description: >-
  Create a new Taskmark task or bug under a story items/ folder, allocate T-NNN or
  B-NNN, calibrate t-shirt size from prior done items, link from the story, and
  update INDEX.md. Use when the user asks for a new task, bug, or work item on
  the Taskmark board.
---

# create-task

## Prerequisites

- Parent story exists; board initialized.
- Read [templates](../taskmark-conventions/references/templates.md), [sizing](../taskmark-conventions/references/sizing.md).

## Steps

1. Resolve parent story; determine `type`: `task` (default) or `bug` from user intent.
2. Gather title, description, acceptance criteria (or repro + fix criteria for bugs), priority, tags.
3. Allocate next `T-NNN` or `B-NNN` by scanning all item files under `taskmark/epics/**/items/`.
4. Create `.../items/{id}-{slug}.md` with Prompt & feedback, Commits, and Work log tables.
5. Set `parent` = story id, `epic` = story’s epic id.
6. **Calibrate size**: scan done items of same type; median of similar → `size`, `size_source: suggested`, `size_basis`.
7. Append link under the story’s Tasks section.
8. Refresh INDEX; recompute story (and epic) size rollup and status per [status-derivation](../taskmark-conventions/references/status-derivation.md).
9. Propagate with `sync-taskmark-repos` when multiple git roots are linked.
10. Reply with id, path, type, size, and basis.

## Bug vs task

- Bug → `type: bug`, id prefix `B-`, sections Description / Repro steps / Fix criteria
- Task → `type: task`, id prefix `T-`, sections Description / Acceptance criteria
