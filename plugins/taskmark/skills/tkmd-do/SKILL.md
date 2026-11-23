---
name: tkmd-do
description: >-
  Implement a Taskmark target using the board item as the spec, without
  committing, pushing, or touching any board file. Works on a branch named
  after the item so the Taskmark App can reconcile it.
---

# tkmd-do

Read `taskmark-conventions` first, including "Reconciliation belongs to the
App".

The board is a read-only reference here. The request brief, the item
description, and its acceptance or fix criteria are the spec. The Taskmark
GitHub / Bitbucket App marks work done from pushes and merged pull requests.

## Non-negotiable safety

- Never run `git commit`, `commit-all-repos.sh`, `git push`, or any equivalent.
- Never edit, rename, move, or delete any existing board file: no status, no
  dates, no resolvers, no checked criteria, no Prompt & feedback, Work log, or
  Commits rows, no text edits. This includes the target and its parents.
- Never create new board items. Planning belongs to `/tkmd-plan`,
  `/tkmd-save`, `/tkmd-plan-do`, and `/tkmd-save-do`.
- Never generate or refresh `INDEX.md`, `SIZING.md`, `VELOCITY.md`, board
  `README.md`, `CHANGELOG.md`, or `REPOS.md`.
- Never run `/tkmd-changelog` or `/tkmd-version`.

## Resolve the target

Accept an ID, markdown path, or unambiguous title. Search frontmatter and
filenames using both legacy IDs (`T-297`) and collision-resistant IDs
(`T-MM-a8f31c2d`), under `requests/*/epics/**` and legacy `epics/**`. On a
request board the request brief of an item is the `brief.md` of the
`requests/<slug>/` folder that contains it.

- Task/bug target: implement that leaf unless it is cancelled or shelved.
  Those terminal outcomes are not implementation scope.
- Story/epic target: derive every descendant task/bug leaf by `parent`/`epic`
  frontmatter before implementation. Every open, non-cancelled, non-shelved
  descendant is mandatory scope: implement all of them, even when the user's
  prompt mentions only the parent ID.
- A target story/epic with no child items is itself a structural leaf; its own
  description and criteria are the spec.
- A target that is already `done`: treat the request as follow-up and just
  implement it. Do not log anything on the item.

If nothing on the board fits the request, do not invent an item. Suggest
`/tkmd-plan-do` (or `/tkmd-plan`) instead.

Read parent context and the request brief, but never write to them.

## Branch

Before changing code in each product repository you touch:

1. The branch id is the target task/bug id. For a story/epic target with
   several leaves, use the story or epic id.
2. If the current branch name already contains that id, stay on it.
3. Otherwise create and switch to `<id>-<short-slug>` from the current branch,
   for example `T-MM-457b0290-login-mockup`. Use a short lowercase slug from
   the item title. If that branch already exists, ask before reusing it.

Never commit or push on that branch.

## Implement

1. Read the target acceptance criteria, the request brief, and relevant
   product code.
2. Make the required product changes.
3. Run checks appropriate to each implemented leaf.
4. For a story/epic target, implement every mandatory leaf. Do not
   voluntarily stop after a subset. A definitive blocker may leave a leaf
   unimplemented; report the whole parent target incomplete.

Before stopping, inspect the board diff. No existing board file may differ.
New product files and normal product-code edits are allowed.

## Report

Return implemented leaves, the criteria each one meets, checks, blockers, the
branch per repository, and uncommitted changes. Tell the user:

- Commits must keep the item id in the branch name or the commit message. The
  `prepare-commit-msg` hook from `npx taskmark hooks install` adds a
  `Task: <id>` trailer automatically.
- The Taskmark App marks the item done when the work is merged and CI passes.
