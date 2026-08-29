---
name: tkmd-version
description: >-
  Promote CHANGELOG Unreleased into a dated SemVer section and set the board
  package.json version. Never tags, publishes, or commits.
---

# tkmd-version

Read `taskmark-conventions` first.

## Non-negotiable safety

- Never run `git commit`, `commit-all-repos.sh`, `git push`, or any equivalent.
- Never create git tags, GitHub Releases, or npm publish.
- Never bump Cursor `plugin.json`, marketplace metadata, or `@taskmark/ui`.
- Never edit epic, story, or leaf markdown.
- Never write or refresh the board `README.md`.
- Never generate or refresh `INDEX.md`, `SIZING.md`, `VELOCITY.md`, or
  `REPOS.md`.

## Locate the board

Same board root as `/tkmd-changelog`: `<product>/taskmark/` or sibling
`<common>-taskmark`. Canonical SemVer lives only on that board’s
`package.json` `version` field. Read `taskmark.writingLanguage` the same way
as `/tkmd-changelog` and keep Unreleased headings in that language.

## Collect notes

If Unreleased is missing or has no bullets, run the same collection and
Unreleased rewrite as `tkmd-changelog` (in the board writing language). If
there is still nothing new, stop and report that; do not bump the version.

## Choose the version

If the user passed an explicit SemVer (for example `/tkmd-version 1.2.0`),
use it.

Otherwise infer from Unreleased work (and the leaves behind it):

- Breaking user-facing change → **major**. On `0.x`, breaking **may** stay
  **minor** instead of jumping to `1.0.0`.
- New user-facing capability → **minor**.
- Bugs, docs, or internal-only work → **patch**.

Read the current board `package.json` `version` (create `0.1.0` only if the
field is missing). Bump that value; do not write versions onto other packages.

## Promote Unreleased

1. Set board `package.json` `version` to the chosen SemVer.
2. Move the Unreleased bullets under a new heading
   `## {version} - YYYY-MM-DD` using today’s UTC date.
3. Place that section **immediately after** Unreleased, newest release first
   (above older `## x.y.z` sections).
4. Leave Unreleased in place with no bullets and no empty `###` categories.
   Unreleased and category headings stay in the board writing language.

Do not edit released sections other than inserting the new one.

## After writing

Report the version, board `package.json` path, changelog path, and that
nothing was tagged, published, or committed. Suggest `/tkmd-commit` when the
user wants git commits.
