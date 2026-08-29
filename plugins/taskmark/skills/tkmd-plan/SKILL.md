---
name: tkmd-plan
description: >-
  Plan Taskmark work from prose by fitting it to the canonical board, avoiding
  duplicates, and creating only the smallest useful hierarchy of new files.
---

# tkmd-plan

Read `taskmark-conventions` first.

## Locate and search the canonical board

Use the existing canonical board. For one product repository it is
`<repo>/taskmark`; for multiple repositories it is the dedicated sibling
`<common>-taskmark` root. If missing, run the `taskmark-init` skill.

Before planning anything new, search all open and done epics, stories, tasks,
and bugs. Compare the request with titles, descriptions, goals, user stories,
acceptance/fix criteria, and parent context.

- If an exact or overlapping item already covers the request, create nothing.
  Report the matching ID and path, then suggest `/tkmd-do` for open work or
  Prompt & feedback on the matching done leaf for follow-up.
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

## Fit new items into the hierarchy

Use the existing parent's real path and write relationships explicitly:

- New task/bug under an existing story:
  `epics/<epic>/stories/<story>/items/<leaf>.md`, with `parent: <story-id>` and
  `epic: <epic-id>`.
- New task/bug directly under an existing epic:
  `epics/<epic>/items/<leaf>.md`, with both `parent: <epic-id>` and
  `epic: <epic-id>`.
- New story under an existing epic:
  `epics/<epic>/stories/<story>/story.md`, with both `parent: <epic-id>` and
  `epic: <epic-id>`.
- New epic:
  `epics/<epic>/epic.md`, with `parent: null` and `epic: null`, only when no
  existing initiative fits.

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

Create all required directories, but write only each new item's own markdown.
Never edit an existing `epic.md`, `story.md`, or leaf. Never write child lists.
Planning is append-by-new-file only: it must not rewrite existing parents or
leaves, even to add links, rollups, logs, status, people, or dates.

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

Every newly planned task/bug leaf must include a `prompt` row summarizing the
current user request. Never write Prompt & feedback on an epic or story file.

If work needs a missing parent, create the smallest explicit hierarchy needed
in the same operation. Creating those new parent files is allowed; modifying
pre-existing parent files is not.

Report a concise hierarchy with IDs, paths, sizes, parent fit, and a short
rationale for the decomposition. If nothing was created, report the exact or
overlapping match and the suggested next action. Do not commit.
