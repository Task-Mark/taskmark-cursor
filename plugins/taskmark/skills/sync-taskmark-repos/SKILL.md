---
name: sync-taskmark-repos
description: >-
  Discover git roots in a multi-folder workspace and copy the Taskmark board
  (taskmark/) into every git project so each repo has the same epics, stories,
  tasks, commits, and logs. Use at session start for multi-root work, after board
  edits, or when the user asks to sync Taskmark across repositories.
---

# sync-taskmark-repos

## When

- Multi-root / multi-folder Cursor workspace with more than one git repository
- After create / start-work / complete-work / log-commits / sync-status
- User asks to copy or sync Taskmark into all projects

## Prerequisites

- Read [multi-repo](../taskmark-conventions/references/multi-repo.md).
- Prefer the helper script: `scripts/sync-taskmark-repos.sh` (from the plugin), or perform equivalent copy steps.

## Steps

1. **Discover git roots** under all workspace folders (directories that contain `.git`). Include nested project folders the user is developing.
2. **Find canonical board**:
   - Prefer path named Canonical in an existing `taskmark/REPOS.md`
   - Else the `taskmark/` with the most epic folders / newest INDEX “Last synced”
   - Else run `taskmark-init` in the primary root first
3. **Write/update `REPOS.md`** on the canonical board listing every git root (Name, Path, Git, Last synced).
4. **Copy** the entire canonical `taskmark/` directory into each other git root (replace destination `taskmark/` with an identical tree). Do not copy unrelated project files.
5. Verify each root has `taskmark/INDEX.md` and matching epic ids.
6. Report which repos were updated and which was canonical.

## Conflict policy

If a non-canonical copy has newer item `updated` timestamps than canonical, warn the user and either:
- promote that copy to canonical for this sync, or
- merge manually before overwriting

Default when timestamps are equal or destination is older: overwrite destination from canonical.

## Single-repo

Still ensure `taskmark/REPOS.md` exists with one row; no copy needed.
