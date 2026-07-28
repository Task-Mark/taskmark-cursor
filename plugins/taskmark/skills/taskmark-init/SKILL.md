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
   - `VELOCITY.md` — [velocity](../taskmark-conventions/references/velocity.md) (seed template; refreshed by recompute)
4. **Seed General:** run `python3 <plugin>/scripts/ensure-general-epic.py <board-root>` so the reserved **General** epic (with epic-level `items/`) exists (see [folder-layout](../taskmark-conventions/references/folder-layout.md)).
5. Run `sync-taskmark-repos` (add `--migrate` when cleaning old per-repo copies or flattening nested boards).
6. Confirm paths; point to `/new-epic` (or `/new-story` / `/new-task`, which soft-attach to General when no parent is named). Tell the user they can open the board UI with `npm i -D @taskmark/ui && npx taskmark serve` (port **8275**) from the product root or board root — no frontend clone required.
7. **Optional UI stub (opt-in only):** if the user wants `npm start`, copy [board-ui-stub `package.json`](../../examples/board-ui-stub/package.json) into the board root (or product root) and adjust the `name` (depends on `@taskmark/ui`). Default boards stay markdown-only without a `package.json`.

## Seed README.md

Include a short intro plus local UI launch (nested `taskmark/` and flat `*-taskmark` both work). Prefer the copy in `examples/sample-board/README.md` (repo) or:

- Title + one paragraph on the board as product memory
- Section **Local board UI**: `npm i -D @taskmark/ui` then `npx taskmark serve` → **http://localhost:8275**; no frontend clone required
- Optional stub: plugin `examples/board-ui-stub/package.json` (`@taskmark/ui`) for `npm start`; default stays markdown-only

## Seed INDEX.md

Use headers with Size | Points | Est (min) | Actual (min) and `—` placeholder rows per [index-format](../taskmark-conventions/references/index-format.md).

## Seed SIZING.md

```markdown
# T-shirt sizing and story points

| Size | Points | Meaning | Seed estimate |
|------|--------|---------|---------------|
| XS | 1 | Trivial | 15 min |
| S | 2 | Small | 30 min |
| M | 3 | Medium | 50 min |
| L | 5 | Large | 90 min |
| XL | 8 | Extra large (prefer split) | 180 min |

Weights for size rollups: XS=1, S=2, M=3, L=4, XL=5.

Sizing suggests size + points; Est uses Current Speed median min/pt when available
(see VELOCITY.md). Seed estimates are fallbacks only.

## Calibration log

| Date | Item | Sized | Points | Est | Actual | Note |
|------|------|-------|--------|-----|--------|------|
| — | — | — | — | — | — | — |
```
