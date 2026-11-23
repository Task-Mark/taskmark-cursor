# Taskmark for Cursor

Taskmark keeps product work as conflict-resistant markdown: requests, with the
epics, stories, tasks, and bugs that deliver them, and meetings remain useful
across chats without generated board files.

This Cursor plugin is one integration. Taskmark works with any AI agent that
can read files (Claude Code, Codex, Copilot, Gemini, Windsurf, Aider, and
others) through a short project instruction: see
[Use Taskmark with any AI agent](https://taskmark.dev/docs/agents).

## Commands

| Command | Purpose |
|---------|---------|
| `/tkmd-init` | Run `npx taskmark init` to set up or repair the board and connect the App |
| `/tkmd-verify` | Migrate an existing board to the current layout |
| `/tkmd-plan` | Search the board and plan the smallest useful hierarchy from prose, in an existing or new request |
| `/tkmd-save` | Turn a Cursor Plan mode plan into board items in an existing or new request, keeping diagrams/visuals |
| `/tkmd-save-do` | Save like `/tkmd-save`, then implement only the newly created items |
| `/tkmd-plan-do` | Plan like `/tkmd-plan`, then implement only the newly created items |
| `/tkmd-do` | Implement a target on an id-named branch without touching the board or committing |
| `/tkmd-changelog` | Rebuild CHANGELOG Unreleased from recent done work and post-release follow-ups |
| `/tkmd-version` | Promote Unreleased and set that SemVer on every linked product |
| `/tkmd-reportme` | Report my done work since the last report into `.reports/` |
| `/tkmd-commit` | Commit dirty linked repositories (the only commit command) |

`/tkmd-plan-do`, `/tkmd-save-do`, `/tkmd-do`, `/tkmd-save`, `/tkmd-verify`, `/tkmd-changelog`,
`/tkmd-version`, and `/tkmd-reportme` never commit or push. Do, plan-do, and save-do do not use an
`in_progress` stage. Changelog and version write `CHANGELOG.md` (and
`/tkmd-version` the same SemVer on every linked product), never a README
changelog.

Agents read the board and plan new items; they never edit existing items.
The Taskmark GitHub / Bitbucket App reconciles status, dates, resolvers,
criteria, Work log, and Commits on each push and merged pull request, and
humans accept its proposals in the review inbox.

## Board layout

One product repository uses `<product>/taskmark/`. Multi-repository workspaces
use a sibling `<common>-taskmark` repository whose root is the board.
`npx taskmark init` sets it up; `/tkmd-init` runs that command and lets you
answer its prompts.

```text
requests/
  <slug>/
    brief.md    # the request: Goal, Why, Done when, Out of scope, Open questions
    epics/      # epics, stories, tasks, and bugs that deliver it
    log/        # append-only request log, written by the App and people
meetings/       # meeting notes, decisions, and tasks
.gitignore
package.json
CHANGELOG.md    # written by /tkmd-changelog and /tkmd-version
README.md       # static project docs from /tkmd-init
server.js
vercel.json
Dockerfile
compose.yaml
REPOS.md        # generated locally and gitignored
.reports/       # /tkmd-reportme output, generated locally and gitignored
```

`/tkmd-plan` and `/tkmd-save` add new epics, stories, and tasks under the
request the work fits, or create a new `requests/<slug>/brief.md` for a new
need. They never edit an existing brief. Delivery stages (`development`,
`testing`, `production`) are written on tasks by the Taskmark App.

Legacy boards keep every epic under `epics/`. On those the plugin keeps
writing under `epics/` and suggests `npx taskmark init`, which migrates the
board to requests (one request per epic).

`/tkmd-init` may write a static project README at the product root
(single-git) or the dedicated `*-taskmark` board root (multi-git). Boards do not generate
`INDEX.md`, `SIZING.md`, `VELOCITY.md`, or a dashboard README.
Parent hierarchy, points, status, logs, contributors, and dates are derived
from item frontmatter and descendant leaves at read time.

## Static sizes

XS=1, S=3, M=5, L=8, XL=13, XXL=21. XXL means the work is not refined or
sprint-ready and should be split before execution.

Items have no estimate or owner property (only a request brief names an
owner). Actual is derived from closed Work log intervals on task/bug leaves
and summed for parent views.

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
