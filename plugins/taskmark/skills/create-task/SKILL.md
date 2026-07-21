---
name: create-task
description: >-
  Create a Taskmark task or bug under a story, allocate T-NNN or B-NNN, suggest
  t-shirt size, story points, and estimate_minutes from history, link from the
  story, and update INDEX. Use when the user asks for a new task or bug.
---

# create-task

## Prerequisites

Parent story exists. Read [templates](../taskmark-conventions/references/templates.md), [sizing](../taskmark-conventions/references/sizing.md).

## Steps

1. Resolve parent story; `type` = `task` or `bug`.
2. Gather title, description, AC or repro/fix criteria, priority, tags.
3. Allocate next `T-NNN` or `B-NNN`.
4. Create item file from template (Prompt & feedback, Commits, Work log).
5. Set `parent` / `epic`.
6. **Calibrate** per sizing ref: `size`, `points`, `estimate_minutes`, sources/basis; `actual_minutes: 0`, `session_cap_minutes: 480`.
7. Link from story Tasks; refresh INDEX; roll up story/epic; refresh VELOCITY if useful.
8. Run `sync-taskmark-repos` only if board location / REPOS needs refresh.
9. Reply with id, path, size, points, estimate_minutes, basis.
