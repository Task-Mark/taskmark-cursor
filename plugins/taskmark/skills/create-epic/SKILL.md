---
name: create-epic
description: >-
  Create a Taskmark epic with points rolled up from stories (no t-shirt size),
  and update INDEX. Use when the user asks for a new epic or initiative.
---

# create-epic

## Prerequisites

`taskmark/` exists (else `taskmark-init`). Read templates + sizing.

## Steps

1. Gather title + goal (and optional scope fields).
2. Allocate next `E-NNN`; create `epic.md` from template.
3. Set `size: null` (epics have **no** t-shirt size). Set `points: 0` until stories exist — points always **sum of child story points**. `estimate_minutes: 0`, `actual_minutes: 0`, `session_cap_minutes: 480`, `points_source: rolled_up`.
4. Empty Commits + Work log headers; refresh INDEX; run `sync-taskmark-repos` only if board location / REPOS needs refresh.
5. Reply with id, path, and note that points/est roll up from stories.

Do not create stories unless asked. Status on create = `backlog`.
