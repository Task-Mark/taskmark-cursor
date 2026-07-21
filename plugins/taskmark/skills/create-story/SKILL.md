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
4. Suggest `size`, `points`, `estimate_minutes` from history; set `actual_minutes: 0`, `session_cap_minutes: 480`.
5. Link from epic; refresh INDEX; roll up epic; multi-repo sync if needed.
6. Reply with id, path, size, points, estimate.
