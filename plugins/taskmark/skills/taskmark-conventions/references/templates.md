# Templates

Copy these structures when creating files. Fill real content; keep section headings exact.

Shared frontmatter fields to include on every item (adjust id/type/parent/epic):

```yaml
size: M
size_source: suggested
size_basis: []
points: 3
points_source: suggested
estimate_minutes: 480
actual_minutes: 0
estimate_source: suggested
estimate_basis: []
session_cap_minutes: 480
```

## Epic (`epic.md`)

```markdown
---
id: E-NNN
type: epic
title: Title here
status: backlog
priority: medium
size: null
size_source: rolled_up
size_basis: [sum:stories]
points: 0
points_source: rolled_up
estimate_minutes: 0
actual_minutes: 0
estimate_source: rolled_up
estimate_basis: [sum:stories]
session_cap_minutes: 480
parent: null
epic: null
owner: ""
blocked: false
cancelled: false
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DDTHH:MM:SSZ
started_at: null
completed_at: null
---

# E-NNN: Title here

## Goal

## Scope

## Out of scope

## Success metrics

## Stories

## Commits

| SHA | Repo | Date (UTC) | Message |
|-----|------|------------|---------|

## Work log

| Session | Actor | Started (UTC) | Ended (UTC) | Summary |
|---------|-------|---------------|-------------|---------|
```

## Story (`story.md`)

```markdown
---
id: S-NNN
type: story
title: Title here
status: backlog
priority: medium
size: M
size_source: suggested
size_basis: []
points: 3
points_source: suggested
estimate_minutes: 480
actual_minutes: 0
estimate_source: suggested
estimate_basis: []
session_cap_minutes: 480
parent: E-NNN
epic: E-NNN
owner: ""
blocked: false
cancelled: false
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DDTHH:MM:SSZ
started_at: null
completed_at: null
---

# S-NNN: Title here

## User story

As a …, I want … so that ….

## Acceptance criteria

- [ ] Criterion

## Tasks

## Prompt & feedback log

| # | When (UTC) | Kind | Summary |
|---|------------|------|---------|

## Commits

| SHA | Repo | Date (UTC) | Message |
|-----|------|------------|---------|

## Work log

| Session | Actor | Started (UTC) | Ended (UTC) | Summary |
|---------|-------|---------------|-------------|---------|
```

When no clearer epic fits, set `parent`/`epic` to the reserved **General** epic id (see [folder-layout](folder-layout.md)). Do not leave stories outside `epics/`.

## Task

```markdown
---
id: T-NNN
type: task
title: Title here
status: backlog
priority: medium
size: M
size_source: suggested
size_basis: []
points: 3
points_source: suggested
estimate_minutes: 480
actual_minutes: 0
estimate_source: suggested
estimate_basis: []
session_cap_minutes: 480
parent: S-NNN
epic: E-NNN
owner: ""
blocked: false
cancelled: false
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DDTHH:MM:SSZ
started_at: null
completed_at: null
---

# T-NNN: Title here

## Description

## Acceptance criteria

- [ ] Criterion

## Notes

## Prompt & feedback log

| # | When (UTC) | Kind | Summary |
|---|------------|------|---------|

## Commits

| SHA | Repo | Date (UTC) | Message |
|-----|------|------------|---------|

## Work log

| Session | Actor | Started (UTC) | Ended (UTC) | Summary |
|---------|-------|---------------|-------------|---------|
```

When no clearer story fits, set `parent` to General’s **Unattached** story and `epic` to General (run `ensure-general-epic.py` first).

## Bug

Same as task, but `type: bug`, id `B-NNN`, and replace Description/Acceptance with Description / Repro steps / Fix criteria. Keep Prompt & feedback, Commits, and Work log.
