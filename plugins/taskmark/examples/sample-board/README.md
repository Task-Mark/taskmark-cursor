# Taskmark board

This folder is the project’s product planning board. Epics, stories, tasks, and bugs live here as markdown so agents and humans share one source of truth.

In multi-git workspaces, the sibling `<common>-taskmark` **repo root is the board** (`INDEX.md` at root — no nested `taskmark/`). Single-git: board stays at `<project>/taskmark/`.

## Local board UI

`taskmark-init` installs `@taskmark/ui` into this folder. Then:

```bash
npx taskmark serve
```

Opens **http://localhost:8275** bound to this board. Or `npm run serve` / `npm start`.

## Deploy on Vercel (Node)

Import this board repo → Framework Preset **Node** (root `server.js`) → `npm install`, no build command.

Use the Taskmark Cursor plugin skills (`taskmark-init`, `create-epic`, `create-story`, `create-task`, `start-work`, `complete-work`, `log-commits`, `sync-taskmark-repos`, `sync-status`) to create and update items.
