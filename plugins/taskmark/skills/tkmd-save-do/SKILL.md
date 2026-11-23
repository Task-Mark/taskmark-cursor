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
- Saving writes new item files only. The do phase follows `tkmd-do` and
  changes no board file, including the items just created.

## Save first

Follow the `tkmd-save` skill in full: locate the Cursor Plan mode plan, search
all open and done epics, stories, tasks, and bugs and every request brief,
place the work in an existing request or a new `requests/<slug>/brief.md` (or
under legacy `epics/` on a board that has no `requests/`), fit existing
hierarchy, allocate IDs, write new files only, and carry plan diagrams and
visuals onto those new items.

Record every markdown path created in this save step, including a new
request brief.

## Skip implementation when save creates nothing

When an exact or overlapping item already covers the plan, create nothing.
Report the matching ID and path. Do not start implementation. Suggest
`/tkmd-do` on that match.

## Implement only newly created items

If save created new item files, run the `tkmd-do` skill only on that new
work:

- A new request brief is context, not an implementation target. Implement the
  new epics, stories, and leaves under it.
- When a new epic or story was created, implement the highest new parent so
  every open, non-cancelled, non-shelved descendant leaf of that parent is
  mandatory scope.
- When only new task/bug leaves were created, implement each newly created
  leaf.
- Do not implement pre-existing open items that save did not create.

During the do phase, follow `tkmd-do` in full: no commit, no push, no
`in_progress`, work on a branch named after the new item id (the highest new
parent id when several leaves were created), and no edits to any board file,
including the items just created and a new request brief. The Taskmark App
marks them done after the work is merged.

Return the saved hierarchy, implemented leaves, checks, blockers, and
uncommitted changes.
