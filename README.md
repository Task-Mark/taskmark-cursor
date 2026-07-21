# Taskmark

Cursor plugin for hierarchical product planning as markdown: **epics → stories → tasks/bugs** under `taskmark/` in your project(s).

Features:

- Convention-enforced board files (frontmatter, IDs, folders)
- Calibrated **t-shirt sizing** (XS–XL) from prior done items
- **Work log** (actor, start, end) on every item
- **Commits log** (SHA, repo, date, message) on every epic, story, task, and bug
- **Prompt & feedback log** on stories, tasks, and bugs
- **Multi-repo sync** — every git project in a multi-folder workspace gets a full `taskmark/` copy
- **Derived status** from acceptance criteria, open sessions, and children
- Always-on project-memory rule so the board informs later product work
- Stop hook that nudges when an agent work session was left open

## Install

### A. Local development (symlink)

```bash
mkdir -p ~/.cursor/plugins/local
ln -s /absolute/path/to/taskmark ~/.cursor/plugins/local/taskmark
```

Then **Developer: Reload Window** in Cursor. Confirm skills/rules appear under **Customize**.

If the symlink does not load, copy the plugin directory into `~/.cursor/plugins/local/taskmark` instead.

### B. Vendor into a project (no marketplace)

Copy plugin components into the consuming repo so the team shares them in git:

```bash
# from the taskmark plugin repo
cp -R skills/* /path/to/your-project/.cursor/skills/
cp -R rules/* /path/to/your-project/.cursor/rules/
mkdir -p /path/to/your-project/.cursor/hooks /path/to/your-project/.cursor/scripts
cp hooks/hooks.json /path/to/your-project/.cursor/hooks.json
cp scripts/check-open-sessions.sh scripts/sync-taskmark-repos.sh /path/to/your-project/.cursor/scripts/
chmod +x /path/to/your-project/.cursor/scripts/*.sh
```

When vendoring the stop hook at project level, use:

```json
{
  "version": 1,
  "hooks": {
    "stop": [
      {
        "command": ".cursor/scripts/check-open-sessions.sh",
        "loop_limit": 1
      }
    ]
  }
}
```

Board data still lives at **`taskmark/`** in each git project (created by `taskmark-init` / synced by `sync-taskmark-repos`), not inside `.cursor/`.

### C. Cursor Marketplace

1. Push this repo to a **public** GitHub repository.
2. Test via local install (A).
3. Submit at [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish).
4. Users install from **Customize → Plugins** (user or workspace scope).

## Quick start

1. Install the plugin (A, B, or C).
2. In a product repo, ask the agent to run **taskmark-init**.
3. **Multi-folder / multi-git workspaces:** run **`/sync-repos`** (`sync-taskmark-repos`) so every git project gets a copy of `taskmark/`.
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
| `/sync-status` | `sync-status` | Recompute status / sizes / INDEX |
| `/board-status` | `taskmark-overview` | Summarize the board |

Also: `taskmark-conventions` (spec), `update-work-item` (edit fields / latches).

## Board layout

```text
taskmark/
├── README.md
├── INDEX.md
├── SIZING.md
├── REPOS.md              # linked git roots
└── epics/
    └── E-001-…/
        ├── epic.md       # includes Commits + Work log
        └── stories/
            └── S-001-…/
                ├── story.md
                └── items/
                    ├── T-001-….md
                    └── B-001-….md
```

See `examples/sample-board/` for a filled-in example (including Commits and `REPOS.md`).

## Multi-repo behavior

When Cursor has multiple project folders (each a git repo):

1. One **canonical** `taskmark/` is the source of truth (`REPOS.md` names it).
2. `sync-taskmark-repos` (script: `scripts/sync-taskmark-repos.sh`) copies that tree into every other git root.
3. Commits tables use the **Repo** column so SHAs from `api`, `web`, etc. stay clear.
4. The always-on project-memory rule requires syncing before/during cross-repo AI development.

## Skills and rules

| Component | Role |
|-----------|------|
| `skills/*` | Agent workflows for init, create, work sessions, commits, multi-repo sync, overview |
| `rules/taskmark-conventions.mdc` | Applies when editing `taskmark/**/*.md` |
| `rules/taskmark-project-memory.mdc` | Always on — link product work to the board; multi-repo copies |
| `hooks/hooks.json` + `scripts/check-open-sessions.sh` | On agent stop, remind if an `agent` work session is still open |
| `scripts/sync-taskmark-repos.sh` | Copy `taskmark/` across discovered git roots |

## License

MIT — see [LICENSE](LICENSE).
