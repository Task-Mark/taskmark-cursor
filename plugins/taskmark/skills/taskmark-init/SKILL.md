---
name: taskmark-init
description: >-
  Initialize conflict-resistant Taskmark storage and board UI without derived
  markdown. Single-git boards live under taskmark/; multi-git boards use a
  dedicated sibling repository root.
---

# taskmark-init

Read `taskmark-conventions` first.

1. Discover product git roots.
   - One root: board = `<product>/taskmark/`.
   - Multiple roots: board = sibling `<common>-taskmark` repository root. Ask
     for the common name when it cannot be derived safely.
2. Create the board directory and `epics/`. An empty `.gitkeep` is allowed.
3. Run:

   ```bash
   python3 <plugin>/scripts/ensure-board-ui.py <board-root> --name <board-package-name>
   ```

   This creates/merges `package.json`, `vercel.json`, optional `server.js`, and
   `.gitignore`. The ignore file must include:

   ```gitignore
   REPOS.md
   node_modules/
   out/
   .taskmark-ui-build/
   ```

4. Run `scripts/sync-taskmark-repos.sh` to generate the local-only
   `REPOS.md`. It contains local paths and no `Last synced` field.
5. Install `@taskmark/ui` as a production dependency:

   ```bash
   npm install @taskmark/ui --save
   ```

6. Verify `npm run build` writes `out/`.

Never create `INDEX.md`, `SIZING.md`, `VELOCITY.md`, a board `README.md`, or
`CHANGELOG.md`. Do not seed a General epic. Existing boards remain compatible
and are not destructively migrated by init.
