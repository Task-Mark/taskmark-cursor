---
name: tkmd-do
description: >-
  Implement a Taskmark target without committing or pushing. Changes only
  executed leaf markdown and marks completed leaves done before stopping.
---

# tkmd-do

Read `taskmark-conventions` first.

## Non-negotiable safety

- Never run `git commit`, `commit-all-repos.sh`, `git push`, or any equivalent.
- Never set an item to `in_progress`; there is no start stage.
- Never edit parent markdown to reflect descendant work.
- Never generate or refresh `INDEX.md`, `SIZING.md`, `VELOCITY.md`, board
  `README.md`, or `REPOS.md`.

## Resolve the target

Accept an ID, markdown path, or unambiguous title. Search frontmatter and
filenames using both legacy IDs (`T-297`) and collision-resistant IDs
(`T-MM-a8f31c2d`).

- Task/bug target: execute that leaf unless it is cancelled or shelved. Those
  terminal outcomes are not implementation scope.
- Story/epic target: derive every descendant task/bug leaf by `parent`/`epic`
  frontmatter before implementation. Every open, non-cancelled, non-shelved
  descendant is mandatory scope: implement and complete all of them, even when
  the user's prompt mentions only the parent ID.
- A target story/epic with no child items is itself a structural leaf and may
  be executed and completed in its own file.

Read parent context, but treat parent fields and sections as immutable.

When the request is follow-up on work already `done`, append Prompt &
feedback (and a Work log row if you spent time) on that existing leaf
instead of inventing a duplicate task. Create a new leaf only when no
open or done task/bug still covers the request.

## Implement

1. Read the target acceptance criteria and relevant product code.
2. Make the required product changes.
3. Run checks appropriate to each executed leaf.
4. For every successfully executed leaf, update that leaf exactly once at the
   end:
   - check acceptance criteria that were actually met;
   - set `status: done`;
   - set `updated` and `completed_at` to current UTC ISO-8601;
   - set `started_at` to the execution start if it is null;
   - add the current git identity to `resolvers`;
   - append concise Prompt & feedback (`prompt` for the user request,
     `feedback` for later notes) and Work log rows when those sections
     exist. Work-log time belongs only to that leaf. Every session that
     did product work must leave at least one prompt row on the chosen
     leaf.
5. Do not mark blocked, skipped, or incomplete leaves done. Report their
   blockers.
6. For a story/epic target, re-scan all descendants before stopping. Success
   requires zero open, non-cancelled, non-shelved task/bug leaves. Do not
   voluntarily stop after a subset, and do not describe the parent target as
   complete while any mandatory descendant remains open. A definitive blocker
   may leave a leaf open, but the command must then report the whole parent
   target incomplete.

Story and epic status are read-time rollups. Completing all descendant leaves
makes those parents done; never write status or lifecycle fields to parent
markdown.

Before stopping, inspect the board markdown diff. Among existing board
markdown, only successfully executed leaf files may differ. New product files
and normal product-code edits are allowed. Do not write parent rollups, logs,
status, resolvers, points, or lifecycle dates; the UI derives them at read time.

Return implemented leaves, checks, blockers, and uncommitted changes.
