# Taskmark board

This folder is the project’s product planning board. Epics, stories, tasks, and bugs live here as markdown so agents and humans share one source of truth.

In multi-git workspaces, the sibling `<common>-taskmark` **repo root is the board** (`INDEX.md` at root — no nested `taskmark/`). Single-git: board stays at `<project>/taskmark/`.

## Local board UI

```bash
npm install @taskmark/ui --save-dev
npx taskmark serve
```

Opens **http://localhost:8275** bound to this board. No need to clone the frontend repo.

Optional (opt-in): add a stub `package.json` with `"start": "taskmark serve"` and `"devDependencies": { "@taskmark/ui": "^0.1.0" }` — see `examples/board-ui-stub/package.json`. Boards stay markdown-first by default.

Use the Taskmark Cursor plugin skills (`taskmark-init`, `create-epic`, `create-story`, `create-task`, `start-work`, `complete-work`, `log-commits`, `sync-taskmark-repos`, `sync-status`) to create and update items.
