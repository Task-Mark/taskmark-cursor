# Taskmark

Cursor plugin for hierarchical product planning as markdown: **epics → stories → tasks/bugs** under `taskmark/` in your project(s).

This repository is a **plugin marketplace** layout:

```text
.cursor-plugin/marketplace.json   # required for “Add local folder”
plugins/taskmark/                 # the plugin itself
  .cursor-plugin/plugin.json
  skills/ rules/ commands/ hooks/ scripts/ assets/
examples/sample-board/            # docs fixture (also copied under the plugin)
```

## Features

- Convention-enforced board files (frontmatter, IDs, folders)
- Calibrated **t-shirt sizing** (XS–XL) from prior done items
- **Work log** (actor, start, end) on every item
- **Commits log** (SHA, repo, date, message) on every epic, story, task, and bug
- **Prompt & feedback log** on stories, tasks, and bugs
- **Multi-repo sync** — every git project in a multi-folder workspace gets a full `taskmark/` copy
- **Commit all** — commit every dirty git project with a very simple one-line message
- **Derived status** from acceptance criteria, open sessions, and children
- Always-on project-memory rule so the board informs later product work
- Stop hook that nudges when an agent work session was left open

## Install

### A. Add local folder (Customize → Plugins)

1. Open **Customize → Plugins**.
2. If an old **taskmark** entry shows “Error loading plugin”, remove it first.
3. Choose **Add local** / select folder.
4. Select this **repository root**: `/Users/menda0/Projects/taskmark`  
   (the folder that contains `.cursor-plugin/marketplace.json`, not `plugins/taskmark`).
5. Enable **taskmark**, then **Developer: Reload Window**.

Cursor clones the marketplace from **git**. After layout changes, commit on `main` before re-adding. If load still fails, delete stale caches and re-add:

```bash
rm -rf ~/.cursor/plugins/cache/taskmark-marketplace
rm -rf ~/.cursor/plugins/marketplaces/_/users/menda0/*
```

### B. Local development (copy into `~/.cursor/plugins/local`)

Cursor **rejects symlinks** that point outside `~/.cursor/plugins/local`. Use a real copy of the plugin package:

```bash
rm -rf ~/.cursor/plugins/local/taskmark
mkdir -p ~/.cursor/plugins/local
rsync -a --delete /absolute/path/to/taskmark/plugins/taskmark/ ~/.cursor/plugins/local/taskmark/
```

Then **Developer: Reload Window**. Re-run the `rsync` after you change plugin files.

### C. Vendor into a project (no marketplace)

```bash
PLUGIN=/path/to/taskmark/plugins/taskmark
cp -R "$PLUGIN/skills/"* /path/to/your-project/.cursor/skills/
cp -R "$PLUGIN/rules/"* /path/to/your-project/.cursor/rules/
mkdir -p /path/to/your-project/.cursor/hooks /path/to/your-project/.cursor/scripts
cp "$PLUGIN/hooks/hooks.json" /path/to/your-project/.cursor/hooks.json
cp "$PLUGIN/scripts/"*.sh /path/to/your-project/.cursor/scripts/
chmod +x /path/to/your-project/.cursor/scripts/*.sh
```

When vendoring the stop hook, point the command at `.cursor/scripts/check-open-sessions.sh`.

Board data still lives at **`taskmark/`** in each product git project (created by `taskmark-init`), not inside `.cursor/`.

### D. Cursor Marketplace

1. Push this repo to a **public** GitHub repository.
2. Test via local install (A or B).
3. Submit at [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish).

## Quick start

1. Install the plugin (A, B, C, or D).
2. In a product repo, ask the agent to run **taskmark-init**.
3. **Multi-folder / multi-git workspaces:** run **`/sync-repos`**.
4. Create and track work:

| Command | Skill | Purpose |
|---------|-------|---------|
| `/new-epic` | `create-epic` | New epic |
| `/new-story` | `create-story` | New story under an epic |
| `/new-task` | `create-task` | New task or bug under a story |
| `/start-work` | `start-work` | Open work session + prompt log |
| `/complete-work` | `complete-work` | Close session, log commits, sync status |
| `/log-commits` | `log-commits` | Append commits to an item |
| `/sync-repos` | `sync-taskmark-repos` | Copy board into every git root |
| `/commit-all` | `commit-all` | Commit every dirty repo (simple one-liner) |
| `/sync-status` | `sync-status` | Recompute status / sizes / INDEX |
| `/board-status` | `taskmark-overview` | Summarize the board |

Also: `taskmark-conventions` (spec), `update-work-item` (edit fields / latches).

## Board layout

```text
taskmark/
├── README.md
├── INDEX.md
├── SIZING.md
├── REPOS.md
└── epics/
    └── E-001-…/
        ├── epic.md
        └── stories/
            └── S-001-…/
                ├── story.md
                └── items/
                    ├── T-001-….md
                    └── B-001-….md
```

See [`examples/sample-board/`](examples/sample-board/) or [`plugins/taskmark/examples/sample-board/`](plugins/taskmark/examples/sample-board/).

## License

MIT — see [LICENSE](LICENSE).
