# Taskmark for Cursor

Taskmark keeps product work as conflict-resistant markdown: epics, stories,
tasks, and bugs remain useful across chats without generated board files.

## Commands

| Command | Purpose |
|---------|---------|
| `/tkmd-init` | Create board storage and UI stubs |
| `/tkmd-plan` | Search the board and plan the smallest useful hierarchy from prose |
| `/tkmd-save` | Turn a Cursor Plan mode plan into board items, keeping diagrams/visuals |
| `/tkmd-plan-do` | Plan like `/tkmd-plan`, then implement only the newly created items |
| `/tkmd-do` | Implement a target and finish executed leaves without committing |
| `/tkmd-shelf` | Discard never-implemented work as shelved without committing |
| `/tkmd-changelog` | Rebuild CHANGELOG Unreleased from recent done work |
| `/tkmd-version` | Promote Unreleased and set the board package.json version |
| `/tkmd-commit` | Commit dirty linked repositories (the only commit command) |

`/tkmd-plan-do`, `/tkmd-do`, `/tkmd-save`, `/tkmd-shelf`, `/tkmd-changelog`,
and `/tkmd-version` never commit or push. Do and plan-do do not use an
`in_progress` stage; shelf keeps discarded work distinct from done. Changelog
and version write `CHANGELOG.md` (and the board `package.json` version), never
a README changelog. Agent sessions log Prompt & feedback on a matching leaf,
including a done task that still fits.

## Board layout

One product repository uses `<product>/taskmark/`. Multi-repository workspaces
use a sibling `<common>-taskmark` repository whose root is the board.

```text
epics/
.gitignore
package.json
CHANGELOG.md    # written by /tkmd-changelog and /tkmd-version
README.md       # static project docs from /tkmd-init
server.js
vercel.json
Dockerfile
compose.yaml
REPOS.md        # generated locally and gitignored
```

`/tkmd-init` writes a static project README at the product root (single-git)
or the dedicated `*-taskmark` board root (multi-git). Boards do not generate
`INDEX.md`, `SIZING.md`, `VELOCITY.md`, or a dashboard README.
Parent hierarchy, points, status, logs, contributors, and dates are derived
from item frontmatter and descendant leaves at read time.

## Static sizes

XS=1, S=3, M=5, L=8, XL=13, XXL=21. XXL means the work is not refined or
sprint-ready and should be split before execution.

There is no estimate or owner property. Actual is derived from closed Work log
intervals on task/bug leaves and summed for parent views.

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
