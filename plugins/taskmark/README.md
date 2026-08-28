# Taskmark

Marketplace package for conflict-resistant markdown product memory in Cursor.

Taskmark exposes exactly four user commands:

- `/tsmk-init` initializes `epics/`, local repository discovery, and board UI
  stubs.
- `/tsmk-create` creates one item or a hierarchy from prose using
  collision-resistant IDs.
- `/tsmk-do` implements a target, never commits or pushes, and finishes only
  executed leaf files.
- `/tsmk-commit` commits dirty linked repositories.

New IDs retain the type and creator identity, for example
`T-MM-a8f31c2d`. Legacy IDs such as `T-297` remain supported.

Sizing is static: XS=1, S=3, M=5, L=8, XL=13, XXL=21. XXL is not sprint-ready
and should be split.

Boards contain `epics/` and UI stubs. `REPOS.md` is generated locally and
gitignored. Taskmark does not generate `INDEX.md`, `SIZING.md`, `VELOCITY.md`,
or a board `README.md`.

Parent relationships and rollups are queried at read time. Creating descendants
does not rewrite parent files; executing work changes only implemented leaves.

For plugin development, run `scripts/rsync-plugin-local.sh` after changes.
