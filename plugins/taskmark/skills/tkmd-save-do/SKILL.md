---
name: tkmd-save-do
description: >-
  Turn a Cursor Plan mode plan into Taskmark items, then implement only the
  newly created items without committing or pushing.
---

# tkmd-save-do

Read `taskmark-conventions` first.

This command composes `tkmd-save` then `tkmd-do`. Keep `/tkmd-save` as the
save-only path. Do not skip the search/dedupe step. New item markdown uses the
board writing language.

## Non-negotiable safety

- Never run `git commit`, `commit-all-repos.sh`, `git push`, or any equivalent.
- Never set an item to `in_progress`; there is no start stage.
- Never generate or refresh `INDEX.md`, `SIZING.md`, `VELOCITY.md`, board
  `README.md`, `CHANGELOG.md`, or `REPOS.md`.
- Saving writes new item files only. The do phase may change only executed
  leaf markdown among existing board files.

## Save first

Follow the `tkmd-save` skill in full: locate the Cursor Plan mode plan, search
all open and done epics, stories, tasks, and bugs, fit existing hierarchy,
allocate IDs, write new files only, and carry plan diagrams and visuals onto
those new items.

Record every markdown path created in this save step.

## Skip implementation when save creates nothing

When an exact or overlapping item already covers the plan, create nothing.
Report the matching ID and path. Do not start implementation. Suggest
`/tkmd-do` for open work or Prompt & feedback on the matching done leaf.

## Implement only newly created items

If save created new item files, run the `tkmd-do` skill only on that new
work:

- When a new epic or story was created, implement the highest new parent so
  every open, non-cancelled, non-shelved descendant leaf of that parent is
  mandatory scope.
- When only new task/bug leaves were created, implement each newly created
  leaf.
- Do not implement pre-existing open items that save did not create.

During the do phase, follow `tkmd-do` safety and completion rules: no commit,
no push, no `in_progress`; mark successfully executed leaves `done` in those
leaf files only.

Return the saved hierarchy, implemented leaves, checks, blockers, and
uncommitted changes.
