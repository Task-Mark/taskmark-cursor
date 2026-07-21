---
name: taskmark-init
description: >-
  Initialize a Taskmark board in the current project by creating taskmark/README.md,
  INDEX.md, SIZING.md, REPOS.md, and an empty epics/ folder. Use when the user asks
  to set up Taskmark, start a planning board, or when create skills find no
  taskmark/ root. In multi-root workspaces, follow with sync-taskmark-repos.
---

# taskmark-init

## When

- User asks to set up Taskmark / a planning board
- Another Taskmark skill needs `taskmark/` and it is missing

## Steps

1. If `taskmark/` already exists with `INDEX.md`, tell the user it is initialized and stop (unless they ask to repair missing files).
2. Create:
   - `taskmark/README.md` — short explanation that this folder is the product board
   - `taskmark/INDEX.md` — empty board index per [index-format](../taskmark-conventions/references/index-format.md)
   - `taskmark/SIZING.md` — t-shirt scale + empty calibration log per [sizing](../taskmark-conventions/references/sizing.md)
   - `taskmark/REPOS.md` — linked git roots per [multi-repo](../taskmark-conventions/references/multi-repo.md) (at least the current repo)
   - `taskmark/epics/` — empty directory (add `.gitkeep` if the VCS needs a file)
3. If the workspace has multiple git roots, immediately follow `sync-taskmark-repos` so every git project gets a copy.
4. Do not create sample epics unless the user asks.
5. Confirm paths created and point the user to `/new-epic` or `create-epic`.

## Seed INDEX.md

```markdown
# Board index

Last synced: <now UTC ISO-8601>

## Epics

| ID | Title | Status | Size | Path |
|----|-------|--------|------|------|
| — | — | — | — | — |

## Stories

| ID | Title | Epic | Status | Size | Path |
|----|-------|------|--------|------|------|
| — | — | — | — | — | — |

## Open work sessions

| Item | Actor | Started (UTC) |
|------|-------|---------------|
| — | — | — |

## Items

| ID | Title | Story | Status | Size | Path |
|----|-------|-------|--------|------|------|
| — | — | — | — | — | — |
```

## Seed REPOS.md

List every git root in the workspace (name = folder basename, path = absolute). Mark one as Canonical. See [multi-repo](../taskmark-conventions/references/multi-repo.md).

