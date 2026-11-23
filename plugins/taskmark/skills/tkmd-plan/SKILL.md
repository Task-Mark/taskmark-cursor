---
name: tkmd-plan
description: >-
  Plan Taskmark work from prose by fitting it to the canonical board (an
  existing request or a new request brief on 2.0 boards), avoiding duplicates,
  and creating only the smallest useful hierarchy of new files.
---

# tkmd-plan

Read `taskmark-conventions` first.

## Locate and search the canonical board

Use the existing canonical board. For one product repository it is
`<repo>/taskmark`; for multiple repositories it is the dedicated sibling
`<common>-taskmark` root. If missing, run the `taskmark-init` skill.

Read `taskmark.writingLanguage` from the board `package.json`. If missing, use
the language the user usually uses with the Cursor agent. Write titles,
descriptions, goals, user stories, and acceptance criteria in that language
even when chat is in another language. Do not translate existing committed
markdown.

Detect the board layout (see "Board layouts" in `taskmark-conventions`):

- **Request board** (Taskmark 2.0): the board has a `requests/` folder. New
  work goes under a request. A legacy `epics/` folder may still sit next to
  it while the board is being migrated; read it, but never create a new epic
  there.
- **Legacy board**: the board has `epics/` and no `requests/`. Keep writing
  under `epics/` exactly as before, and tell the user that `npx taskmark init`
  migrates the board to requests.

Before planning anything new, search all open and done epics, stories, tasks,
and bugs, wherever they live (`requests/*/epics/**` and legacy `epics/**`).
On a request board also search every request brief
(`requests/<slug>/brief.md`): its `title`, `aliases`, Goal, Why, Done when,
and Out of scope. Compare the request with titles, descriptions, goals, user
stories, acceptance/fix criteria, and parent context.

- If an exact or overlapping item already covers the request, create nothing.
  Report the matching ID and path, then suggest `/tkmd-do` on that match, for
  open work or for follow-up on done work.
- Prefer attaching work to an existing fitting story or epic over creating a
  parallel hierarchy.
- Create a new epic only for a distinct initiative that fits nowhere on the
  existing board.

## Reason from prose

Infer the smallest useful hierarchy rather than requiring the user to name an
item type:

- initiative/outcome → epic
- user-visible capability → story
- executable unit → task
- defect/regression → bug

Broad initiatives should become cohesive stories, each split into independently
executable task/bug leaves with clear, observable acceptance or fix criteria.
Do not create parent levels that add no useful grouping. Ask only when ambiguity
would materially change scope, placement, or the resulting hierarchy.

## Use sizing to refine the plan

Use static sizing as a decomposition driver for every independently executable
leaf:

- XS / 1: trivial, isolated change
- S / 3: small, understood change
- M / 5: moderate change with a few moving parts
- L / 8: large change spanning multiple parts
- XL / 13: very large; strongly prefer splitting into cohesive leaves
- XXL / 21: not refined or sprint-ready; never leave it unrefined

Split XXL work before writing files. Strongly split XL work unless there is a
clear reason it is one indivisible executable unit. Do not derive sizes from
elapsed time, velocity, or historical medians. Items created with children use
`size: null` and `points: null`; their values are read-time rollups.

## Choose the request (request boards only)

Every new epic, story, task, or bug on a request board belongs to exactly one
request. Decide which one before writing:

- **Existing request.** When the work serves the goal of an existing request
  (match on brief title, `aliases`, Goal, Why, and Done when, not just on
  words), add the new items under `requests/<slug>/epics/...` of that request.
  Never edit its `brief.md`, not even to add scope, a Done when line, or an
  open question; mention in the report what the brief does not yet say.
  Small fixes, bugs, and chores that need no brief of their own fit the
  board's `maintenance` request when it exists. Do not use it for a real new
  need.
- **New request.** When the work is a new need that no request covers, create
  a new request folder `requests/<slug>/` with a `brief.md` (template below)
  plus its epics, stories, and tasks.

Ask only when the choice between an existing request and a new one would
materially change scope or placement.

### New request brief

Pick `<slug>` as a short lowercase hyphenated form of the request title
(ASCII letters, digits, and hyphens, at most 48 characters). If
`requests/<slug>/` already exists, append `-2`, `-3`, and so on. The request
id is `R-<slug>`, the same id style the migration and the App use; it never
collides because the folder name is unique.

```yaml
---
id: R-<slug>
type: request
title: <title>
status: <proposed|ready>
requested_by:
  - name: "<who asked: the named person, else git user.name>"
    email: "<email when known>"
owner:
  - name: "<git user.name, unless the user names an owner>"
    email: "<git user.email>"
    initials: "<identity>"
created: <UTC YYYY-MM-DD>
updated: <UTC ISO-8601>
forecast: null
tags: []
aliases: []
source_meetings: []
links: []
---
```

Use `status: ready` when the plan creates executable leaves and Done when is
clear; use `proposed` while open questions still block the scope. Never write
`building`, `shipped`, `shelved`, or `cancelled`: delivery status and stages
come from the Taskmark App and the leaves.

The body, in the board writing language:

```markdown
# <title>

## Goal

<the outcome the requester wants>

## Why

<the reason or context behind it>

## Done when

- [ ] <observable outcome>

## Out of scope

- <what this request does not cover>

## Open questions

- [ ] <question, or "_None yet._">
```

Do not create `requests/<slug>/log/` entries, `meetings/` files, `stage`, or
`shipped_at`. The App and people write those.

## Fit new items into the hierarchy

Use the existing parent's real path and write relationships explicitly. On a
request board `<root>` is `requests/<slug>/epics` of the chosen request (or the
request that already holds the parent); on a legacy board `<root>` is
`epics`:

- New task/bug under an existing story:
  `<root>/<epic>/stories/<story>/items/<leaf>.md`, with `parent: <story-id>`
  and `epic: <epic-id>`.
- New task/bug directly under an existing epic:
  `<root>/<epic>/items/<leaf>.md`, with both `parent: <epic-id>` and
  `epic: <epic-id>`.
- New story under an existing epic:
  `<root>/<epic>/stories/<story>/story.md`, with both `parent: <epic-id>` and
  `epic: <epic-id>`.
- New epic:
  `<root>/<epic>/epic.md`, with `parent: null` and `epic: null`, only when no
  existing initiative fits. A new request always gets at least one new epic.

An existing epic that still lives under legacy `epics/` on a request board
stays a valid parent; new descendants go next to it in that epic's folder. Do
not move it.

Never soft-attach to a reserved or generic epic merely because placement is
unclear. Search for semantic fit first; ask only if the remaining ambiguity
materially changes scope.

## Allocate IDs

For every new item run:

```bash
python3 <plugin>/scripts/allocate-id.py <E|S|T|B> <board-root> --cwd <product-repo>
```

Never use a shared counter or `NEXT_IDS` file. Existing `E-NNN`, `S-NNN`,
`T-NNN`, and `B-NNN` IDs remain valid parents.

## Write files

Create all required directories, but write only each new item's own markdown
(and, for a new request, its new `brief.md`). Never edit an existing
`epic.md`, `story.md`, or leaf, and never edit an existing request `brief.md`
or meeting file. Never write child lists.
Planning is append-by-new-file only: it must not rewrite existing parents or
leaves, even to add links, rollups, logs, status, people, or dates. After the
files are written, they belong to the board like any other item: later
sessions treat them as read-only (see "Reconciliation belongs to the App" in
`taskmark-conventions`).

Use common frontmatter:

```yaml
---
id: <id>
type: <epic|story|task|bug>
title: <title>
status: backlog
priority: <low|medium|high|critical>
size: <XS|S|M|L|XL|XXL|null>
points: <1|3|5|8|13|21|null>
parent: <parent-id|null>
epic: <epic-id|null>
reporters:
  - name: "<git user.name>"
    email: "<git user.email>"
    initials: "<identity>"
resolvers: []
blocked: false
cancelled: false
tags: []
created: <UTC YYYY-MM-DD>
updated: <UTC ISO-8601>
started_at: null
completed_at: null
---
```

Epic/story files contain only their description, goal/user story, and
acceptance criteria. Task/bug leaves additionally contain:

```markdown
## Prompt & feedback

| When (UTC) | Kind | Author | Summary |
|------------|------|--------|---------|

## Commits

| SHA | Repo | Date (UTC) | Author | Message |
|-----|------|------------|--------|---------|

## Work log

| Actor | Started (UTC) | Ended (UTC) | Summary |
|-------|---------------|-------------|---------|
```

Leave those tables empty. The Taskmark App fills Commits and Work log from
pushes and merged pull requests; agents never write rows into them.

If work needs a missing parent, create the smallest explicit hierarchy needed
in the same operation. Creating those new parent files is allowed; modifying
pre-existing parent files is not.

Report a concise hierarchy with IDs, paths, sizes, parent fit, the request
the work landed in (existing or new, with its id and path), and a short
rationale for the decomposition. On a legacy board, suggest
`npx taskmark init` to migrate it to requests. If nothing was created, report the exact or
overlapping match and the suggested next action. Do not commit.
