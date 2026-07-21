---
name: create-story
description: >-
  Create a Taskmark user story under an epic with suggested size, story points,
  and estimate_minutes, link from the epic, and update INDEX. Use when the user
  asks for a new story.
---

# create-story

## Prerequisites

Parent epic exists. Read [templates](../taskmark-conventions/references/templates.md), [sizing](../taskmark-conventions/references/sizing.md).

## Steps

1. Resolve parent epic.
2. Gather title, user story, AC, priority, tags.
3. Allocate next `S-NNN`; create `story.md` from template.
4. Suggest initial `size`, `points`, `estimate_minutes` from 30-day velocity × points (else seeds) when the story has **no tasks yet**. Once tasks exist, **points = sum of task/bug points** (and est rolls up) via sync/`recompute-actuals`. Set `actual_minutes: 0`, `session_cap_minutes: 480`.
5. Link from epic; refresh INDEX; roll up epic **points** (sum of stories; epic has no size); run `sync-taskmark-repos` only if board location / REPOS needs refresh.
6. Reply with id, path, size, points, estimate.
