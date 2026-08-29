---
name: tkmd-plan-do
description: >-
  Plan Taskmark work from prose, then implement only the newly created items
  without committing or pushing.
---

# tkmd-plan-do

Read `taskmark-conventions` first.

This command composes `tkmd-plan` then `tkmd-do`. Keep `/tkmd-plan` as the
plan-only path. Do not skip the search/dedupe step. New item markdown uses the
board writing language.

## Non-negotiable safety

- Never run `git commit`, `commit-all-repos.sh`, `git push`, or any equivalent.
- Never set an item to `in_progress`; there is no start stage.
- Never generate or refresh `INDEX.md`, `SIZING.md`, `VELOCITY.md`, board
  `README.md`, `CHANGELOG.md`, or `REPOS.md`.
- Planning writes new item files only. The do phase may change only executed
  leaf markdown among existing board files.

## Plan first

Follow the `tkmd-plan` skill in full: locate the canonical board, search all
open and done epics, stories, tasks, and bugs, fit existing hierarchy, allocate
IDs, and write new files only.

Record every markdown path created in this planning step.

## Skip implementation when planning creates nothing

When an exact or overlapping item already covers the request, create nothing.
Report the matching ID and path. Do not start implementation. Suggest
`/tkmd-do` for open work or Prompt & feedback on the matching done leaf.

## Implement only newly created items

If planning created new item files, run the `tkmd-do` skill only on that new
work:

- When a new epic or story was created, implement the highest new parent so
  every open, non-cancelled, non-shelved descendant leaf of that parent is
  mandatory scope.
- When only new task/bug leaves were created, implement each newly created
  leaf.
- Do not implement pre-existing open items that planning did not create.

During the do phase, follow `tkmd-do` safety and completion rules: no commit,
no push, no `in_progress`; mark successfully executed leaves `done` in those
leaf files only.

Return the planned hierarchy, implemented leaves, checks, blockers, and
uncommitted changes.
