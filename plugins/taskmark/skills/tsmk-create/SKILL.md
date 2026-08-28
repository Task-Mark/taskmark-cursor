---
name: tsmk-create
description: >-
  Create one Taskmark epic, story, task, or bug, or a complete hierarchy from
  prose. Uses collision-resistant IDs and writes new item files only.
---

# tsmk-create

Read `taskmark-conventions` first.

## Interpret the request

Accept an explicit item type or infer a useful hierarchy from prose:

- initiative/outcome → epic
- user-visible capability → story
- executable unit → task
- defect/regression → bug

The command may create one item or an epic with any number of nested stories
and task/bug leaves. Ask only when ambiguity would materially change scope.

## Locate the board

Use the existing canonical board. For one product repository it is
`<repo>/taskmark`; for multiple repositories it is the dedicated sibling
`<common>-taskmark` root. If missing, run the `taskmark-init` skill.

## Allocate IDs

For every new item run:

```bash
python3 <plugin>/scripts/allocate-id.py <E|S|T|B> <board-root> --cwd <product-repo>
```

Never use a shared counter or `NEXT_IDS` file. Existing `E-NNN`, `S-NNN`,
`T-NNN`, and `B-NNN` IDs remain valid parents.

## Size leaves

Choose exactly one static size for every item created without children
(including a standalone epic or story):

- XS / 1: trivial, isolated change
- S / 3: small, understood change
- M / 5: moderate change with a few moving parts
- L / 8: large change spanning multiple parts
- XL / 13: very large; splitting strongly preferred
- XXL / 21: not refined or sprint-ready; split before execution

Do not derive estimates from elapsed time, velocity, or historical medians.
Items created with children use `size: null` and `points: null`; their values
are read-time rollups. Do not persist rollups.

## Write files

Create all required directories, but write only each new item's own markdown.
Never edit an existing `epic.md`, `story.md`, or leaf. Never write child lists.

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

If a single story/task needs a missing parent, create the smallest explicit
hierarchy needed as part of the same operation. Creating those new parent files
is allowed; modifying pre-existing parent files is not.

Report the IDs and paths created. Do not commit.
