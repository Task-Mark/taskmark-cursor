---
name: taskmark-init
description: >-
  Initialize a Taskmark board (INDEX, SIZING, REPOS, epics). Single-git:
  under <project>/taskmark/. Multi-git: at sibling <common>-taskmark repo root
  (flat). Use when setting up Taskmark or when create skills find no board.
---

# taskmark-init

## Steps

1. Discover git roots. Decide mode per [multi-repo](../taskmark-conventions/references/multi-repo.md):
   - **One product git root:** target = that root’s `taskmark/`.
   - **Multiple product git roots:** ensure sibling `<common>-taskmark` (ask user if name ambiguous; `git init` if new), target = **that repo’s root** (board files at root — no nested `taskmark/`).
2. If target already has `INDEX.md`, tell the user it is initialized and stop (unless they ask to repair missing files).
3. Create under the target:
   - `README.md`
   - `INDEX.md` — [index-format](../taskmark-conventions/references/index-format.md)
   - `SIZING.md` — [sizing](../taskmark-conventions/references/sizing.md)
   - `REPOS.md` — [multi-repo](../taskmark-conventions/references/multi-repo.md)
   - `epics/` (optional `.gitkeep`)
4. **Do not** create `VELOCITY.md` (velocity/time-estimate mechanism removed — S-057).
5. **Seed General:** run `python3 <plugin>/scripts/ensure-general-epic.py <board-root>` so the reserved **General** epic (with epic-level `items/`) exists (see [folder-layout](../taskmark-conventions/references/folder-layout.md)).
6. Run `sync-taskmark-repos` (add `--migrate` when cleaning old per-repo copies or flattening nested boards).
7. Confirm paths; point to `/new-epic` (or `/new-story` / `/new-task`, which soft-attach to General when no parent is named).

## Seed INDEX.md

Use headers with Size | Points | Est (min) | Actual (min) and `—` placeholder rows per [index-format](../taskmark-conventions/references/index-format.md).

## Seed SIZING.md

```markdown
# T-shirt sizing and story points

| Size | Points | Meaning |
|------|--------|---------|
| XS | 1 | Trivial |
| S | 2 | Small |
| M | 3 | Medium |
| L | 5 | Large |
| XL | 8 | Extra large (prefer split) |

Weights for size rollups: XS=1, S=2, M=3, L=4, XL=5.

Sizing suggests **size + points only**. Do not suggest `estimate_minutes` from size
(velocity/time-estimate mechanism removed).

## Calibration log

| Date | Item | Sized | Points | Note |
|------|------|-------|--------|------|
```
