---
name: sync-taskmark-repos
description: >-
  Ensure the Taskmark board is in the correct location for the workspace mode:
  <project>/taskmark for single-git, or sibling <common>-taskmark repo root
  for multi-git. Generate gitignored local REPOS.md without timestamps.
---

# sync-taskmark-repos

## When

- Multi-root / multi-folder Cursor workspace
- After init or migration of board layout
- User asks to sync Taskmark repos / ensure board location

## Steps

1. Read `taskmark-conventions`.
2. Run `scripts/sync-taskmark-repos.sh [--name COMMON] [workspace ...]`.
3. The script discovers git roots, locates a board by its `epics/` directory,
   writes local `REPOS.md`, and ensures the board `.gitignore` contains it.
4. It never copies board content, rewrites item markdown, or generates derived
   markdown.
5. Report mode, canonical board path, and linked repositories.

## Ambiguous name

The script exits `2` when the common name cannot be derived. Ask the user, then:

```bash
scripts/sync-taskmark-repos.sh --name <common> [workspace…]
```

## Single-repo

Generate `REPOS.md` under `<project>/taskmark/` only. It is local state and
must remain gitignored.
