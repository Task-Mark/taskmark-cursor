---
name: sync-taskmark-repos
description: >-
  Ensure the Taskmark board is in the correct location for the workspace mode:
  <project>/taskmark for single-git, or sibling <common>-taskmark repo root
  (flat — no nested taskmark/) for multi-git. Refresh REPOS.md. Never copy the
  board into every product repo. Use at session start, after board layout
  changes, or when the user asks to sync Taskmark repos.
---

# sync-taskmark-repos

## When

- Multi-root / multi-folder Cursor workspace
- After init or migration of board layout
- User asks to sync Taskmark repos / ensure board location

## Prerequisites

- Read [multi-repo](../taskmark-conventions/references/multi-repo.md).
- Prefer `scripts/sync-taskmark-repos.sh` from the plugin package.

## Steps

1. **Discover git roots** under workspace folders.
2. **Classify** product roots vs dedicated `*-taskmark` board roots.
3. **Single product root:** board at `<project>/taskmark/`; refresh `REPOS.md`. Do **not** create a sibling `-taskmark` project.
4. **Multiple product roots:**
   - Derive `<common_project_name>` (shared parent basename, else shared prefix). If ambiguous, **ask the user** (or re-run with `--name`).
   - Ensure sibling `<common>-taskmark` exists; `git init` if needed.
   - Board files live at **`<common>-taskmark/` root** (`INDEX.md`, `epics/`, …) — **not** under `<common>-taskmark/taskmark/`.
   - Flatten any legacy nested `taskmark/` folder inside the dedicated repo.
   - Write `REPOS.md` at the board repo root listing the board + product roots.
   - Do **not** copy the board into product repos.
5. **`--migrate`:** promote richest existing board into the dedicated project (flat), then delete leftover `taskmark/` directories from product repos.
6. **Vercel / board UI stubs:** if the canonical board has `INDEX.md` but is missing `server.js` or `vercel.json`, run:
   ```bash
   python3 <plugin>/scripts/ensure-board-ui.py <canonical-board-root>
   ```
   (Do not overwrite customized files unless the user asks for `--force`.) Prefer full `taskmark-init` when the board itself is missing.
7. Report mode, canonical path, and common name.

## Ambiguous name

Script exits `2` when the common name cannot be derived. Ask the user for the common project name, then:

```bash
scripts/sync-taskmark-repos.sh --name <common> --migrate [workspace…]
```

## Single-repo

Refresh `REPOS.md` under `<project>/taskmark/` only.
