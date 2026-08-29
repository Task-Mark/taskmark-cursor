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
3. Choose the board writing language. Ask the user; any language is allowed.
   Default if they do not pick one: the language they usually use with the
   Cursor agent. If `package.json` already has `taskmark.writingLanguage`, keep
   it unless they explicitly name a different language. Write agent-authored
   board markdown in that language even when chat is in another one.
4. Run:

   ```bash
   python3 <plugin>/scripts/ensure-board-ui.py <board-root> --name <board-package-name> --writing-language "<language>"
   ```

   This creates/merges `package.json`, `vercel.json`, optional `server.js`,
   Docker stubs (`Dockerfile`, `compose.yaml`, `.dockerignore`), and `.gitignore`.
   Add `--replace-writing-language` only when the user explicitly changes a
   language that is already stored. Omitting `--writing-language` on a repair
   leaves an existing `taskmark.writingLanguage` untouched. Other `package.json`
   keys must not be clobbered. The ignore file must include:

   ```gitignore
   REPOS.md
   node_modules/
   out/
   .taskmark-ui-build/
   ```

5. Run `scripts/sync-taskmark-repos.sh` to generate the local-only
   `REPOS.md`. It contains local paths and no `Last synced` field.
6. Install `@taskmark/ui` as a production dependency:

   ```bash
   npm install @taskmark/ui --save
   ```

7. Verify `npm run build` writes `out/`.
8. Write or repair the **static project README** from
   `examples/static-project-readme.md`, in the board writing language.

   Location (static project docs, never a generated dashboard):

   - Single-git: product-root `README.md` (not nested `taskmark/README.md`).
   - Multi-git: `README.md` at the dedicated sibling `*-taskmark` board root
     (this repo is the board product). Do not write a Last synced / Current
     speed / open-work dashboard there.

   Fill in: Taskmark’s purpose; the workspace’s product repositories by **name
   and role** (not gitignored local absolute paths); local run (`npm install`,
   `npx taskmark serve` / `dev`, port 8275); production `npm run build` / `out/`;
   Vercel via the board `vercel.json` static `out/` flow; Docker
   (`docker compose up --build` on the board stubs); standalone
   `npx @taskmark/ui` (workspace/picker vs bound board). Do not tell users to
   `npx taskmark` unless `@taskmark/ui` is installed locally.

   Do **not** overwrite a richer hand-written README. Create or replace only
   when the file is missing, thinner than this template, or still a generated
   dashboard (Last synced, Current speed, open-work list, README changelog).
   Docker stubs must exist on the board if the README documents Docker.

Never create `INDEX.md`, `SIZING.md`, `VELOCITY.md`, a generated board
dashboard README, or `CHANGELOG.md`. Do not seed a General epic. Existing
boards remain compatible and are not destructively migrated by init.
