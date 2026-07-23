---
name: create-story
description: >-
  Create a Taskmark user story (optional epic) with suggested size, story points,
  and estimate_minutes, link from the epic, and update INDEX. Use when the user
  asks for a new story.
---

# create-story

## Prerequisites

Board exists (else `taskmark-init`). Read [templates](../taskmark-conventions/references/templates.md), [sizing](../taskmark-conventions/references/sizing.md), [folder-layout](../taskmark-conventions/references/folder-layout.md) (General epic).

## Steps

1. **Resolve parent epic (soft-attach):**
   - If the user names an epic id/title/path, use it.
   - Else infer from prompt + open board context (matching epic titles/tags, active epic in conversation).
   - Else run `python3 <plugin>/scripts/ensure-general-epic.py <board-root>` and attach under **General**.
2. Gather title, user story, AC, priority, tags.
3. Allocate next `S-NNN`; create `story.md` from template under that epic’s `stories/`.
4. Suggest initial `size`, `points`, `estimate_minutes` from 30-day velocity × points (else seeds) when the story has **no tasks yet**. Once tasks exist, **points = sum of task/bug points** (and est rolls up) via sync/`recompute-actuals`. Set `actual_minutes: 0`, `session_cap_minutes: 480`.
5. Set `parent` / `epic` to the resolved epic id. Link from epic; refresh INDEX; roll up epic **points** (sum of stories; epic has no size); run `sync-taskmark-repos` only if board location / REPOS needs refresh.
6. Reply with id, path, size, points, estimate, and **assigned epic** (including General when used).
