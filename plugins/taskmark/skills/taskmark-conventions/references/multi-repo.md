# Multi-repo boards

Taskmark supports **multi-root / multi-git** workspaces (several folders, each its own git repository). Every git project the user is actively developing must keep a **copy** of the `taskmark/` board so product memory travels with that repo.

## Model

1. Discover git roots in the workspace (directories containing `.git`, including nested project folders in a multi-root Cursor window).
2. Pick a **canonical** board: prefer an existing `taskmark/` with the richest `INDEX.md` / most epics; otherwise the workspace folder the user named as primary; otherwise the first root that already has `taskmark/`.
3. Ensure **every** active git root has a full copy of `taskmark/` (same tree: README, INDEX, SIZING, REPOS, epics/…).
4. Track linked roots in `taskmark/REPOS.md` (identical content in each copy).

## `taskmark/REPOS.md`

```markdown
# Linked repositories

Canonical: api

| Name | Path | Git | Last synced (UTC) |
|------|------|-----|-------------------|
| api | /Users/me/work/api | yes | 2026-07-21T15:00:00Z |
| web | /Users/me/work/web | yes | 2026-07-21T15:00:00Z |
| worker | /Users/me/work/worker | yes | 2026-07-21T15:00:00Z |
```

- **Name** = short repo id used in Commits tables
- **Path** = absolute path to the git root
- **Canonical** = which copy is the source of truth when merging divergent edits

## Sync rules

1. Before starting product work in a multi-root workspace, run `sync-taskmark-repos` (or follow that skill) so every git root has `taskmark/`.
2. After meaningful board edits (create, start-work, complete-work, log-commits, sync-status), **propagate** the updated `taskmark/` tree from the canonical (or the repo you just edited) to all other linked roots.
3. Prefer **whole-tree copy** of `taskmark/` (not cherry-picked files) so copies stay identical.
4. Do not copy `.git` or unrelated project files — only the `taskmark/` directory.
5. If two copies diverged, prefer the copy with the newer `INDEX.md` “Last synced” / file `updated` timestamps; mention the conflict to the user before overwriting.
6. Single-repo workspaces: still create `REPOS.md` with one row; Commits `Repo` column uses that name.

## Agent obligations

- When the workspace has multiple folders / git roots and the user is developing with AI across them, **do not** keep Taskmark in only one repo.
- Use the `sync-taskmark-repos` skill at session start for multi-root work and after board mutations.
- Record commits with the correct **Repo** name from `REPOS.md`.
