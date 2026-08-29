---
name: tkmd-shelf
description: >-
  Shelve discarded Taskmark work without implementing, committing, or pushing.
  Writes only eligible task/bug leaf markdown.
---

# tkmd-shelf

Read `taskmark-conventions` first.

Prompt rows and any new leaf prose use the board writing language.

## Non-negotiable safety

- Never run `git commit`, `commit-all-repos.sh`, `git push`, or any equivalent.
- Never edit epic or story markdown.
- Never check acceptance criteria or describe shelved work as implemented.
- Never set `cancelled: true`; shelving uses the distinct terminal
  `status: shelved`.
- Never generate or refresh `INDEX.md`, `SIZING.md`, `VELOCITY.md`, board
  `README.md`, `CHANGELOG.md`, or `REPOS.md`.

## Resolve the target

Accept an ID, markdown path, or unambiguous title. Search frontmatter and
filenames using both legacy and collision-resistant IDs.

- Task/bug target: shelve it unless it is already done, cancelled, or shelved.
- Story/epic target: derive descendants by `parent` and `epic` frontmatter,
  then select every task/bug leaf that is not done, cancelled, or shelved.
- Story/epic targets with no eligible descendants are no-ops. Do not edit the
  parent file to manufacture a stored parent status.

Read parent context, but treat parent fields and sections as immutable.

## Shelve

For every selected leaf:

1. Set `status: shelved`.
2. Set `updated` and `completed_at` to the current UTC ISO-8601 timestamp.
3. Preserve `cancelled: false`, `started_at`, `resolvers`, and all acceptance
   criteria. Shelved means discarded without implementation.
4. Append a concise `prompt` row when a Prompt & feedback section exists.
5. Do not append implementation work or commit rows.

For a story or epic, re-scan all descendants before stopping. Success requires
zero open, non-cancelled, non-shelved task/bug leaves. Never edit parent
markdown: all-shelved parent status is a read-time rollup.

Before stopping, inspect the board markdown diff. Among existing board
markdown, only leaves selected for shelving may differ.

Return shelved leaves, no-op leaves, blockers, and uncommitted changes.
