# Commits log

Required on **every** epic, story, task, and bug.

Records git commits that implemented or related to the item. In multi-repo workspaces, include the **repo** column so commits from different git roots stay distinguishable.

```markdown
## Commits

| SHA | Repo | Date (UTC) | Message |
|-----|------|------------|---------|
| a1b2c3d | api | 2026-07-21T14:30:00Z | feat(auth): add login endpoint |
| e4f5g6h | web | 2026-07-21T15:10:00Z | feat(auth): wire login form to API |
```

## Rules

1. Append-only — do not rewrite or delete past rows (unless fixing a clear mistake).
2. **SHA** = short (7+) or full commit hash from that repo.
3. **Repo** = short name for the git root (folder name, or name from `taskmark/REPOS.md`). Use `.` or the single repo name when only one git root exists.
4. **Date** = commit author/committer date in UTC ISO-8601 when available.
5. **Message** = subject line only (first line of the commit message).
6. Log commits when they land (after `git commit` / merge) via `log-commits` or as part of `complete-work`.
7. Prefer commits that clearly belong to this item; if a commit spans multiple items, log it on each relevant item (or the lowest-level task/bug plus optionally the parent story).
8. Story/epic commit lists may include child commits that were also logged on tasks — that is OK for overview; prefer logging primarily on the leaf task/bug and rolling notable SHAs up only when useful.

## How to collect

From a git root, after work on an item:

```bash
git log --since="<session-started>" --pretty=format:'%h|%cI|%s'
```

Map each line into a Commits table row with the repo short name.
