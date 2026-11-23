---
name: taskmark-conventions
description: >-
  Canonical conflict-resistant Taskmark markdown conventions, for 2.0 request
  boards and legacy epic boards. Use before initializing, creating,
  implementing, or committing Taskmark work.
---

# Taskmark conventions

## Board location

- One product git root: `<product>/taskmark/`.
- Multiple product git roots: sibling `<common>-taskmark` repository root.
- A board contains `requests/` and `meetings/` (2.0 request board) or legacy
  `epics/`, plus UI stubs. It does not contain `INDEX.md`, `SIZING.md`,
  `VELOCITY.md`, or a generated dashboard `README.md`.
- `npx taskmark init` sets the board up (run by `/tkmd-init`); the plugin
  hand-creates the scaffold only when npm/npx is unavailable.
- `/tkmd-init` may write a **static project README** (purpose, product
  repositories, run, build, deploy). Single-git: product-root `README.md`,
  not nested `taskmark/README.md`. Multi-git: `README.md` at the dedicated
  sibling `*-taskmark` board root. That file is static docs, not a generated
  dashboard. Init does not clobber a richer hand-written README; it creates
  or repairs when the file is missing or still a generated dashboard.
- `CHANGELOG.md` at the board root is allowed. Only `/tkmd-changelog` and
  `/tkmd-version` write it. Do not generate changelog sections in a README.
- `REPOS.md` is local-generated and must be listed in the board `.gitignore`.
- `.reports/` holds personal `/tkmd-reportme` output. It is local-generated and
  must be listed in the board `.gitignore`.

## Board layouts

Taskmark 2.0 boards group work under the request it delivers. Legacy boards
keep every epic under `epics/`. A board being migrated can have both; both are
read.

Request board (2.0):

```text
requests/<slug>/brief.md                     # the request: what, why, done when
requests/<slug>/epics/<epic-id>-<slug>/...   # epics, stories, tasks, bugs
requests/<slug>/log/<date>-<slug>.md         # append-only request log
meetings/<date>-<slug>.md                    # meetings, decisions, tasks
```

- A folder under `requests/` is a request only when it has `brief.md`.
- The brief frontmatter holds `id` (`R-<slug>`), `type: request`, `title`,
  `status` (`proposed`, `ready`, `building`, `shipped`, `shelved`,
  `cancelled`), `requested_by`, `owner`, `created`, `updated`, `forecast`,
  `tags`, `aliases` (old ids, such as the epic a request was migrated from),
  `source_meetings`, and `links`. Its sections are Goal, Why, Done when, Out of
  scope, and Open questions.
- Epics, stories, tasks, and bugs keep exactly the same files and frontmatter
  as on a legacy board; they just live under the request. Relationships still
  come from `parent` and `epic`; the request comes from the folder.
- Agents may create a **new** request (`brief.md` with status `proposed` or
  `ready`) and new items under a request. They never edit an existing brief.
- Request logs, meetings, task `stage` (`development`, `testing`,
  `production`), and `shipped_at` are written by the Taskmark App and by
  people, never by agents.
- `npx taskmark init` migrates a legacy board (one request per epic, the epic
  id kept as an alias). On a legacy board the plugin keeps writing under
  `epics/` and suggests running it.

Legacy board:

```text
epics/<epic-id>-<slug>/...
```

## Board writing language

- Stored on the board in committed `package.json` as `taskmark.writingLanguage`.
  Any language is allowed (a name or tag such as `English` or `pt`).
- `/tkmd-init` asks the user to pick a language. If they do not pick one, use
  the language they usually use with the Cursor agent. Re-running init keeps a
  stored value unless they explicitly choose a different language.
- Read that field at the start of every `/tkmd-*` session that writes markdown.
  If it is missing, follow the same init default. Do not invent a second
  ad-hoc locale.
- Write new work-item markdown (titles, descriptions, goals, user stories,
  acceptance/fix criteria), changelog prose, the static project README, and
  other agent-authored board markdown in that stored language even when the
  chat is in another language.
- Do not translate existing committed markdown unless the current task
  explicitly rewrites that file.

## IDs and paths

New IDs use `<type>-<identity>-<random>`, for example `T-MM-a8f31c2d`.
Type is `E`, `S`, `T`, or `B`; identity is 2 to 12 uppercase letters/digits from
the git user; random is at least 8 lowercase hexadecimal characters. Generate
with `scripts/allocate-id.py` and retry if any existing path or frontmatter
already contains the candidate.

Existing zero-padded IDs such as `E-022` and `T-297` remain valid. Readers must
accept both:

```regex
^[ESBT]-(?:[0-9]{3}|[A-Z0-9]{2,12}-[a-z0-9]{8,})$
```

Request ids are `R-<slug>`, unique because the request folder name is
unique on the board.

Paths, where `<root>` is `requests/<slug>/epics` on a request board and
`epics` on a legacy board:

```text
<root>/<epic-id>-<slug>/epic.md
<root>/<epic-id>-<slug>/stories/<story-id>-<slug>/story.md
<root>/<epic-id>-<slug>/stories/<story-id>-<slug>/items/<task-or-bug-id>-<slug>.md
<root>/<epic-id>-<slug>/items/<task-or-bug-id>-<slug>.md
```

Relationships come from `parent` and `epic` frontmatter. Never add child lists
or rollups to parent markdown.

## Static sizing

| Size | Points | Meaning |
|------|--------|---------|
| XS | 1 | Trivial, isolated change |
| S | 3 | Small, understood change |
| M | 5 | Moderate change with a few moving parts |
| L | 8 | Large change spanning multiple parts |
| XL | 13 | Very large; splitting is strongly preferred |
| XXL | 21 | Not refined or sprint-ready; split before execution |

Use this map only. Do not calibrate from velocity or write time estimates.
Parent size, points, status, people, logs, and lifecycle dates are read-time
views derived from descendants.

Items (epics, stories, tasks, bugs) have no estimate or owner property; only
a request brief names an `owner`. Actual is not frontmatter: the UI sums
valid closed Started → Ended intervals from leaf Work log rows. Parent
Actual is the sum of descendant leaf Actual values.

## Status

- `backlog`, `blocked`, and `in_progress` are incomplete.
- `done`, `shelved`, and `cancelled` are terminal.
- `done` means implemented; `shelved` means deliberately discarded without
  implementation; `cancelled` remains a separate legacy/latch outcome.
- Parent status is derived from descendants: a terminal mix containing at least
  one done leaf rolls up to `done`; without done, any shelved leaf rolls up to
  `shelved`; all cancelled leaves roll up to `cancelled`.
- Hide-completed and completeness sorting treat all three terminal statuses as
  complete.

## Reconciliation belongs to the App

- Agents read and plan. The board is the reference: the request brief, the
  item description, and its acceptance or fix criteria guide the work.
- The Taskmark GitHub / Bitbucket App reconciles. On each push and merged pull
  request it marks items done and writes status, stages, dates, resolvers,
  checked criteria, Work log rows, Commits rows, and request log entries.
- Humans accept the App's proposals in the review inbox, and shelve or cancel
  items by hand when work is dropped.
- Agents never change an existing epic, story, task, bug, request brief, or
  meeting file in any way: no status, dates, resolvers, checked criteria,
  Prompt & feedback, Work log, or Commits rows, and no text edits.
- Agents help the App match work through branch names and commit messages
  that contain the item id.

## Write boundaries

- Create writes only files for newly created items (and a new request
  `brief.md` on a request board). Once written, they are read-only like every
  other item.
- Implementation writes product code only, never board files.
- Commits, work notes, resolvers, status, and lifecycle dates live on leaf
  files and are written by the App. Parent views aggregate descendant leaves.
- `/tkmd-plan` and `/tkmd-save` put new work under an existing request or a
  new request on a request board, and under `epics/` on a legacy board.
- `/tkmd-save` creates new item files from a Cursor Plan mode plan and never
  implements, commits, or pushes.
- `/tkmd-save-do` runs `/tkmd-save` then `/tkmd-do` only on newly created
  items; it never commits or pushes and never uses `in_progress`.
- `/tkmd-plan-do` runs `/tkmd-plan` then `/tkmd-do` only on newly created
  items; it never commits or pushes and never uses `in_progress`.
- `/tkmd-do` works on a branch whose name contains the item id, never touches
  board files, never commits or pushes, never uses `in_progress`, and never
  writes `CHANGELOG.md`.
- `/tkmd-verify` migrates an existing board (scaffold repair, delete leftover
  generated files, strip retired frontmatter and parent child lists). It is
  the only command that rewrites existing item files, it is maintainer-only,
  and it never touches status, logs, commits, or criteria. It never commits
  or pushes and never creates `INDEX.md`, `SIZING.md`, `VELOCITY.md`, or
  `CHANGELOG.md`.
- `/tkmd-changelog` rebuilds Unreleased in board-root `CHANGELOG.md` from
  done leaves completed after the last release and from post-cutoff Work log
  rows (written by the App) on already-done leaves, in the board writing
  language. It never edits item markdown, the README, commits, or pushes.
- `/tkmd-version` promotes Unreleased into `## x.y.z - YYYY-MM-DD`, sets that
  SemVer on the board `package.json`, every linked product-root `package.json`,
  and the Cursor plugin `plugin.json`, and never tags, publishes, commits, or
  pushes.
- `/tkmd-reportme` writes only `.reports/report-YYYYMMDD.md` on the board,
  covering the current git identity's done leaves since the previous report in
  the board writing language. It never implements, edits item markdown, writes
  `CHANGELOG.md` or the README, commits, or pushes.
- `/tkmd-commit` is the only user command that commits.

## Changelog wording

Board `CHANGELOG.md` uses Keep a Changelog structure in the **board writing
language** (see `taskmark.writingLanguage`), not a hardcoded locale.

- Unreleased heading and category headings (`Added`, `Changed`, `Deprecated`,
  `Removed`, `Fixed`, `Security`, or the equivalent in the stored language).
- Dated releases stay `## x.y.z - YYYY-MM-DD`.
- Preserve existing dated sections when rebuilding Unreleased.

Each Unreleased bullet is one user-visible outcome in past tense. Newly
completed leaves (completed after the last dated release) are phrased from
the user story, acceptance criteria, or title. Follow-up work on a leaf
already completed on or before that cutoff is phrased from post-cutoff Work
log summaries, not from the original title. Do not repeat an outcome that already appears in a released section.
Visible text must not include work-item codes (`T-` / `B-` / `S-` / `E-`).
Related leaves or follow-ups from the same story may be merged when that
reads better.

Example (English board): `A button to filter completed tasks was added.`
Translate headings and bullets when the stored language is not English.
