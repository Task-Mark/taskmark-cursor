# Taskmark for Cursor

Taskmark keeps product work as conflict-resistant markdown: epics, stories,
tasks, and bugs remain useful across chats without generated board files.

## Commands

| Command | Purpose |
|---------|---------|
| `/tsmk-init` | Create board storage and UI stubs |
| `/tsmk-create` | Create one item or a hierarchy from prose |
| `/tsmk-do` | Implement a target and finish executed leaves without committing |
| `/tsmk-commit` | Commit dirty linked repositories |

These are the only user-facing commands. `/tsmk-do` never commits or pushes and
does not use an `in_progress` stage.

## Board layout

One product repository uses `<product>/taskmark/`. Multi-repository workspaces
use a sibling `<common>-taskmark` repository whose root is the board.

```text
epics/
.gitignore
package.json
server.js
vercel.json
REPOS.md        # generated locally and gitignored
```

Boards do not generate `INDEX.md`, `SIZING.md`, `VELOCITY.md`, or `README.md`.
Parent hierarchy, points, status, logs, contributors, and dates are derived
from item frontmatter and descendant leaves at read time.

## Static sizes

XS=1, S=3, M=5, L=8, XL=13, XXL=21. XXL means the work is not refined or
sprint-ready and should be split before execution.

## Install

Add this repository root as a local Cursor plugin marketplace. For local plugin
development, copy the package with:

```bash
plugins/taskmark/scripts/rsync-plugin-local.sh
```

The board UI is installed as `@taskmark/ui`; `npm run build` emits static files
under `out/`.

## License

MIT
