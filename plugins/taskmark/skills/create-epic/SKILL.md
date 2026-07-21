---
name: create-epic
description: >-
  Create a Taskmark epic with suggested size, story points, and estimate_minutes,
  and update INDEX. Use when the user asks for a new epic or initiative.
---

# create-epic

## Prerequisites

`taskmark/` exists (else `taskmark-init`). Read templates + sizing.

## Steps

1. Gather title + goal (and optional scope fields).
2. Allocate next `E-NNN`; create `epic.md` from template.
3. Suggest `size`, `points`, `estimate_minutes`; `actual_minutes: 0`, `session_cap_minutes: 480`.
4. Empty Commits + Work log headers; refresh INDEX; run `sync-taskmark-repos` only if board location / REPOS needs refresh.
5. Reply with id, path, size, points, estimate.

Do not create stories unless asked. Status on create = `backlog`.
