# Taskmark

Cursor plugin for hierarchical product planning as markdown: **epics → stories → tasks/bugs** under `taskmark/` in your project(s).

This repository is a **plugin marketplace** layout:

```text
.cursor-plugin/marketplace.json   # required for “Add local folder”
plugins/taskmark/                 # the plugin itself
  .cursor-plugin/plugin.json
  skills/ rules/ commands/ hooks/ scripts/ assets/
examples/sample-board/            # docs fixture (also under the plugin)
```

## Features

- Convention-enforced board files (frontmatter, IDs, folders)
- **T-shirt sizing** + **Fibonacci story points** with calibrated suggestions
- **Estimate vs actual minutes** from work-log sessions (never calendar span)
- **Idle auto-cap** — abandoned sessions end at next-day 12:00 UTC; session cap default 480 min
- **VELOCITY.md** — team median minutes/point and delivery ETA
- Work log, commits log, prompt/feedback logs
- Single- or multi-git board location (`<common>-taskmark` sibling) + commit-all
- Derived status; project-memory rule; stop hook for open/idle sessions

## Install

### A. Add local folder (Customize → Plugins)

1. Open **Customize → Plugins**.
2. Remove any broken **taskmark** entry first.
3. **Add local** → select this repo root: `…/taskmark-cursor` (folder with `.cursor-plugin/marketplace.json`).
4. Enable **taskmark**, then **Developer: Reload Window**.

After layout changes, **commit** before re-adding (Cursor packages from git). Clear stale caches if needed:

```bash
rm -rf ~/.cursor/plugins/cache/taskmark-marketplace
rm -rf ~/.cursor/plugins/marketplaces/_/users/menda0/*
```

### B. Local development (copy)

Cursor rejects external symlinks. Copy the plugin package:

```bash
plugins/taskmark/scripts/rsync-plugin-local.sh
# or:
rsync -a --delete /absolute/path/to/taskmark-cursor/plugins/taskmark/ ~/.cursor/plugins/local/taskmark/
```

After editing the plugin in this repo, the agent must run **`sync-plugin-local`** (`/sync-plugin-local`) so the local install stays current. Reload the window if new skills do not appear.

### C. Vendor / D. Marketplace

See prior docs: copy skills/rules/hooks into a project `.cursor/`, or publish the public git repo.

## Quick start

1. Install the plugin.
2. Run **taskmark-init** in a product repo.
3. Multi-git workspaces: **`/sync-repos`**.
4. Commands:

| Command | Skill | Purpose |
|---------|-------|---------|
| `/new-epic` | `create-epic` | New epic |
| `/new-story` | `create-story` | New story |
| `/new-task` | `create-task` | New task or bug |
| `/start-work` | `start-work` | Open session (idle-closes stale first) |
| `/complete-work` | `complete-work` | Close session + actual minutes |
| `/sync-status` | `sync-status` | Status, actuals, INDEX, VELOCITY |
| `/velocity` | `taskmark-velocity` | Team speed / ETA |
| `/sync-plugin-local` | `sync-plugin-local` | Rsync plugin → `~/.cursor/plugins/local` |
| `/board-status` | `taskmark-overview` | Board summary |
| `/log-commits` | `log-commits` | Record commits |
| `/sync-repos` | `sync-taskmark-repos` | Ensure board location + REPOS.md |
| `/commit-all` | `commit-all` | Commit every dirty repo |

## Board layout

```text
taskmark/
├── README.md
├── INDEX.md
├── SIZING.md
├── VELOCITY.md
├── REPOS.md
└── epics/…
```

Effort rules: billable work-log minutes only; idle deadline = next UTC day at 12:00; `session_cap_minutes` default 480.

## License

MIT — see [LICENSE](LICENSE).
