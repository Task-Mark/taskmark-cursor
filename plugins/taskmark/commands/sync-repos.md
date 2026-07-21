---
name: sync-repos
description: Ensure Taskmark board location for single vs multi-git workspaces and refresh REPOS.md
---

# Sync Taskmark across repos

Follow the `sync-taskmark-repos` skill. Single-git: board at `<project>/taskmark/`. Multi-git: sibling `<common>-taskmark` **repo root is the board** (no nested `taskmark/`); refresh `REPOS.md`. Never copy into product repos. Ask for `--name` when ambiguous; use `--migrate` to remove leftovers and flatten nested boards.
