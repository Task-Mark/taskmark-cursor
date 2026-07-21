---
name: create-epic
description: >-
  Create a new Taskmark epic under taskmark/epics/ with epic.md, allocate the next
  E-NNN id, suggest t-shirt size, and update INDEX.md. Use when the user asks for a
  new epic, initiative, or large product theme on the Taskmark board.
---

# create-epic

## Prerequisites

- Ensure `taskmark/` exists (run `taskmark-init` if not).
- Read [templates](../taskmark-conventions/references/templates.md), [sizing](../taskmark-conventions/references/sizing.md), [folder-layout](../taskmark-conventions/references/folder-layout.md).

## Steps

1. Gather title, goal, scope, out of scope, success metrics, priority, tags (ask only for missing required bits: at least title + goal).
2. Scan `taskmark/epics/**/epic.md` for the highest `E-NNN`; next id = max+1 (start at `E-001`).
3. Build slug from title; create `taskmark/epics/{id}-{slug}/epic.md` from the epic template.
4. Suggest `size` from done epics (or default `M`); set `size_source` / `size_basis`.
5. Set `status: backlog`, timestamps `created` / `updated` to now, empty Commits and Work log tables (headers only).
6. Link nothing under Stories yet.
7. Refresh `taskmark/INDEX.md` (add epic row).
8. If multiple git roots are linked, run `sync-taskmark-repos` so every repo copy is updated.
9. Reply with id, path, and suggested size.

## Do not

- Create stories automatically unless the user asks in the same turn.
- Hand-set status to anything other than `backlog` on create.
