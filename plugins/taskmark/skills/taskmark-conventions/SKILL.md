---
name: taskmark-conventions
description: >-
  Canonical conflict-resistant Taskmark markdown conventions. Use before
  initializing, creating, implementing, or committing Taskmark work.
---

# Taskmark conventions

## Board location

- One product git root: `<product>/taskmark/`.
- Multiple product git roots: sibling `<common>-taskmark` repository root.
- A board contains `epics/` plus UI stubs. It does not contain `INDEX.md`,
  `SIZING.md`, `VELOCITY.md`, or a generated dashboard `README.md`.
- `/tkmd-init` writes a **static project README** (purpose, product
  repositories, run, build, deploy). Single-git: product-root `README.md`,
  not nested `taskmark/README.md`. Multi-git: `README.md` at the dedicated
  sibling `*-taskmark` board root. That file is static docs, not a generated
  dashboard. Init does not clobber a richer hand-written README; it creates
  or repairs when the file is missing or still a generated dashboard.
- `CHANGELOG.md` at the board root is allowed. Only `/tkmd-changelog` and
  `/tkmd-version` write it. Do not generate changelog sections in a README.
- `REPOS.md` is local-generated and must be listed in the board `.gitignore`.

## Board writing language

- Stored on the board in committed `package.json` as `taskmark.writingLanguage`.
  Any language is allowed (a name or tag such as `English` or `pt`).
- `/tkmd-init` asks the user to pick a language. If they do not pick one, use
  the language they usually use with the Cursor agent. Re-running init keeps a
  stored value unless they explicitly choose a different language.
- Read that field at the start of every `/tkmd-*` session that writes markdown.
  If it is missing, follow the same init default. Do not invent a second
  ad-hoc locale.
- Write work-item markdown (titles, descriptions, goals, user stories,
  acceptance/fix criteria, Prompt & feedback summaries, work-log summaries),
  changelog prose, the static project README, and other agent-authored board
  markdown in that stored language even when the chat is in another language.
- Do not translate existing committed markdown unless the current task
  explicitly rewrites that file.

## IDs and paths

New IDs use `<type>-<identity>-<random>`, for example `T-MM-a8f31c2d`.
Type is `E`, `S`, `T`, or `B`; identity is 2–12 uppercase letters/digits from
the git user; random is at least 8 lowercase hexadecimal characters. Generate
with `scripts/allocate-id.py` and retry if any existing path or frontmatter
already contains the candidate.

Existing zero-padded IDs such as `E-022` and `T-297` remain valid. Readers must
accept both:

```regex
^[ESBT]-(?:[0-9]{3}|[A-Z0-9]{2,12}-[a-z0-9]{8,})$
```

Paths:

```text
epics/<epic-id>-<slug>/epic.md
epics/<epic-id>-<slug>/stories/<story-id>-<slug>/story.md
epics/<epic-id>-<slug>/stories/<story-id>-<slug>/items/<task-or-bug-id>-<slug>.md
epics/<epic-id>-<slug>/items/<task-or-bug-id>-<slug>.md
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

There is no estimate or owner property. Actual is not frontmatter: the UI
sums valid closed Started → Ended intervals from leaf Work log rows. Parent
Actual is the sum of descendant leaf Actual values.

## Status

- `backlog`, `blocked`, and `in_progress` are incomplete.
- `done`, `shelved`, and `cancelled` are terminal.
- `done` means implemented; `shelved` means deliberately discarded without
  implementation; `cancelled` remains a separate legacy/latch outcome.
- `/tkmd-shelf` sets only eligible task/bug leaves to `status: shelved` with
  `completed_at` set. It does not check acceptance criteria, set
  `cancelled: true`, or edit parent markdown.
- Parent status is derived from descendants: a terminal mix containing at least
  one done leaf rolls up to `done`; without done, any shelved leaf rolls up to
  `shelved`; all cancelled leaves roll up to `cancelled`.
- Hide-completed and completeness sorting treat all three terminal statuses as
  complete.

## Write boundaries

- Create writes only files for newly created items.
- Execution writes only the task/bug leaf files actually implemented.
- Epic and story files are immutable while adding or executing descendants.
- Prompt/feedback, commits, work notes, implementers, status, and lifecycle
  dates live on leaf files. Parent views aggregate descendant leaves.
- Every agent session that changes product work appends Prompt & feedback on a
  matching leaf: prefer an open task/bug that fits, else a done leaf whose
  scope still covers the change, else create a new task/bug. Never write those
  rows on `epic.md` or `story.md`.
- `/tkmd-save` creates new item files from a Cursor Plan mode plan and never
  implements, commits, or pushes.
- `/tkmd-plan-do` runs `/tkmd-plan` then `/tkmd-do` only on newly created
  items; it never commits or pushes and never uses `in_progress`.
- `/tkmd-do` never commits or pushes, never uses `in_progress`, and never
  writes `CHANGELOG.md`.
- `/tkmd-shelf` never implements, commits, pushes, or edits parent markdown.
- `/tkmd-changelog` rebuilds Unreleased in board-root `CHANGELOG.md` from
  recent done leaves, in the board writing language. It never edits item
  markdown, the README, commits, or pushes.
- `/tkmd-version` promotes Unreleased into `## x.y.z - YYYY-MM-DD`, sets that
  SemVer on the board `package.json`, every linked product-root `package.json`,
  and the Cursor plugin `plugin.json`, and never tags, publishes, commits, or
  pushes.
- `/tkmd-commit` is the only user command that commits.

## Changelog wording

Board `CHANGELOG.md` uses Keep a Changelog structure in the **board writing
language** (see `taskmark.writingLanguage`), not a hardcoded locale.

- Unreleased heading and category headings (`Added`, `Changed`, `Deprecated`,
  `Removed`, `Fixed`, `Security`, or the equivalent in the stored language).
- Dated releases stay `## x.y.z - YYYY-MM-DD`.
- Preserve existing dated sections when rebuilding Unreleased.

Each Unreleased bullet is one user-visible outcome in past tense, taken from
the user story, acceptance criteria, or title. Visible text must not include
work-item codes (`T-` / `B-` / `S-` / `E-`). Related leaves from the same story
may be merged when that reads better.

Example (English board): `A button to filter completed tasks was added.`
Translate headings and bullets when the stored language is not English.
