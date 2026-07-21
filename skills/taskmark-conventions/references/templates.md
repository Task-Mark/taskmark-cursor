# Templates

Copy these structures when creating files. Fill real content; keep section headings exact.

## Epic (`epic.md`)

```markdown
---
id: E-NNN
type: epic
title: Title here
status: backlog
priority: medium
size: M
size_source: suggested
size_basis: []
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

## Bug

Same as task, but `type: bug`, id `B-NNN`, and replace Description/Acceptance with:

```markdown
## Description

## Repro steps

1. …

## Fix criteria

- [ ] Criterion

## Notes
```

Keep **Prompt & feedback**, **Commits**, and **Work log** sections on bugs as on tasks.
