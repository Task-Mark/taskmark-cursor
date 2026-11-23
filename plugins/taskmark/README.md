# Taskmark

Marketplace package for conflict-resistant markdown product memory in Cursor.

Taskmark exposes these user commands:

- `/tkmd-init` initializes `epics/`, local repository discovery, and board UI
  stubs, records a writing language (any language; default is the language
  the user usually uses with the Cursor agent), and writes or repairs a
  static project README (not a generated dashboard).
- `/tkmd-verify` migrates an existing board to the current layout: repairs
  scaffold like init, deletes leftover generated files, and strips retired
  frontmatter and parent child lists. It is maintainer-only, never touches
  status, logs, commits, or criteria, and never commits or pushes.
- `/tkmd-plan` searches the canonical board and creates the smallest useful
  hierarchy from prose using collision-resistant IDs.
- `/tkmd-save` turns a Cursor Plan mode plan into epic, story, task, and bug
  files and carries plan diagrams and visuals onto those items. It never
  implements, commits, or pushes.
- `/tkmd-save-do` runs the same save as `/tkmd-save`, then implements only the
  newly created items like `/tkmd-do`. If save creates nothing, it reports the
  match and skips implementation.
- `/tkmd-plan-do` runs the same planning as `/tkmd-plan`, then implements only
  the newly created items like `/tkmd-do`. If planning creates nothing, it
  reports the match and skips implementation.
- `/tkmd-do` implements a target using the item as the spec, on a branch
  whose name contains the item id. It never touches board files, commits, or
  pushes.
- `/tkmd-changelog` rebuilds the Unreleased section of board-root
  `CHANGELOG.md` from recent done work and from post-release Work log
  follow-ups on already-done leaves, in the board writing language. It never
  writes the README, commits, or pushes.
- `/tkmd-version` promotes Unreleased into a dated `x.y.z` section and sets
  that SemVer on the board `package.json`, every linked product-root
  `package.json`, and the Cursor plugin `plugin.json`. It never tags,
  publishes, or commits.
- `/tkmd-reportme` reports what the current git identity finished since the
  previous report as human-readable bullets in `.reports/report-YYYYMMDD.md`.
  Those files are gitignored and personal; the command never commits or pushes.
- `/tkmd-commit` commits dirty linked repositories. It is the only command
  that commits.

Chat language and board writing language are independent. Work items,
changelog, README, and other agent-written board markdown always use the
language stored as `taskmark.writingLanguage` on the board, even when the
conversation is in another language.

New IDs retain the type and creator identity, for example
`T-MM-a8f31c2d`. Legacy IDs such as `T-297` remain supported.

Sizing is static: XS=1, S=3, M=5, L=8, XL=13, XXL=21. XXL is not sprint-ready
and should be split.

Taskmark has no estimate or owner property. Actual is the sum of closed Work
log intervals stored on task/bug leaves; parent Actual is derived from leaves.

Boards contain `epics/` and UI stubs. `REPOS.md` and `.reports/` are generated
locally and gitignored. Taskmark does not generate `INDEX.md`, `SIZING.md`, `VELOCITY.md`,
or a dashboard README. `/tkmd-init` writes a static project README at the
product root (single-git) or the dedicated `*-taskmark` board root
(multi-git). Release notes live in `CHANGELOG.md`, written only by
`/tkmd-changelog` and `/tkmd-version`.

Parent relationships and rollups are queried at read time. Creating descendants
does not rewrite parent files.

Agents treat existing items as read-only. The Taskmark GitHub / Bitbucket App
reconciles status, dates, resolvers, criteria, Work log, and Commits on each
push and merged pull request, and humans accept its proposals in the review
inbox. Keep the item id in the branch name or commit message; the
`prepare-commit-msg` hook from `npx taskmark hooks install` adds a
`Task: <id>` trailer.

For plugin development, run `scripts/rsync-plugin-local.sh` after changes.
