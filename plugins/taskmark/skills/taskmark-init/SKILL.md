---
name: taskmark-init
description: >-
  Initialize a Taskmark board (INDEX, SIZING, REPOS, epics), install
  @taskmark/ui, and scaffold Vercel Node stubs (server.js + vercel.json) so
  `npx taskmark serve` and Vercel Framework Preset: Node work. Single-git: under
  <project>/taskmark/. Multi-git: at sibling <common>-taskmark repo root
  (flat). Use when setting up Taskmark or when create skills find no board.
---

# taskmark-init

## Steps

1. Discover git roots. Decide mode per [multi-repo](../taskmark-conventions/references/multi-repo.md):
   - **One product git root:** target = that root’s `taskmark/`.
   - **Multiple product git roots:** ensure sibling `<common>-taskmark` (ask user if name ambiguous; `git init` if new), target = **that repo’s root** (board files at root — no nested `taskmark/`).
2. If target already has `INDEX.md`:
   - Do **not** recreate board markdown (`INDEX.md`, epics, etc.).
   - **Still always run** step 7 (Install board UI + **Vercel init**) so missing `server.js` / `vercel.json` / `@taskmark/ui` are repaired — unless the user explicitly asked to skip UI install.
3. Create under the target (first-time only):
   - `README.md`
   - `INDEX.md` — [index-format](../taskmark-conventions/references/index-format.md)
   - `SIZING.md` — [sizing](../taskmark-conventions/references/sizing.md)
   - `REPOS.md` — [multi-repo](../taskmark-conventions/references/multi-repo.md)
   - `epics/` (optional `.gitkeep`)
   - `VELOCITY.md` — [velocity](../taskmark-conventions/references/velocity.md) (seed template; refreshed by recompute)
4. **Seed General:** run `python3 <plugin>/scripts/ensure-general-epic.py <board-root>` so the reserved **General** epic (with epic-level `items/`) exists (see [folder-layout](../taskmark-conventions/references/folder-layout.md)).
5. Run `sync-taskmark-repos` (add `--migrate` when cleaning old per-repo copies or flattening nested boards).
6. Confirm paths; point to `/new-epic` (or `/new-story` / `/new-task`, which soft-attach to General when no parent is named).
7. **Install board UI + Vercel init (required):** under the board root (flat `*-taskmark` root, or nested `…/taskmark/`):
   1. Run the stub helper (copies/merges `package.json`, `server.js`, `vercel.json`, ensures `.gitignore` has `node_modules/`):
      ```bash
      python3 <plugin>/scripts/ensure-board-ui.py <board-root> --name <sensible-package-name>
      ```
      Example names: `taskmark-taskmark`, `<project>-taskmark`. This **is** Taskmark’s Vercel init (Framework Preset: **Node** via root `server.js`) — do **not** run `vercel init` (that downloads unrelated Vercel examples).
   2. Install the UI from the board root:
      ```bash
      npm install @taskmark/ui --save
      ```
      If the registry returns **404 / not found** and a local package with `"name": "@taskmark/ui"` exists in the workspace (commonly sibling `taskmark-frontend`):
      ```bash
      npm install <absolute-or-relative-path-to-@taskmark/ui> --save
      ```
      Tell the user which source was used.
   3. Confirm `npx taskmark serve` works → **http://localhost:8275**. Confirm `server.js` + `vercel.json` exist for Vercel (import board repo → Framework Preset **Node**).

## Seed README.md

Include a short intro plus local UI launch (nested `taskmark/` and flat `*-taskmark` both work). Prefer the copy in `examples/sample-board/README.md` (repo) or:

- Title + one paragraph on the board as product memory
- Section **Local board UI**: after init, `npx taskmark serve` → **http://localhost:8275** (`npm i @taskmark/ui` is done by init)
- Note `npm start` / `npm run serve` work when the stub `package.json` is present; Vercel uses Framework Preset **Node** + `server.js` (scaffolded by `ensure-board-ui.py`)

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
