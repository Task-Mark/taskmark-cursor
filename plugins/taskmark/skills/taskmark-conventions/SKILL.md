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
  `SIZING.md`, `VELOCITY.md`, or a board `README.md`.
- `REPOS.md` is local-generated and must be listed in the board `.gitignore`.

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
- `/tsmk-do` never commits or pushes and never uses `in_progress`.
- `/tsmk-commit` is the only user command that commits.
