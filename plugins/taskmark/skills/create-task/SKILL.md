---
name: create-task
description: >-
  Create a Taskmark task or bug (optional story), allocate T-NNN or B-NNN, suggest
  t-shirt size, story points, and estimate_minutes from history, link from the
  story, and update INDEX. Use when the user asks for a new task or bug.
---

# create-task

## Prerequisites

Board exists (else `taskmark-init`). Read [templates](../taskmark-conventions/references/templates.md), [sizing](../taskmark-conventions/references/sizing.md), [folder-layout](../taskmark-conventions/references/folder-layout.md) (General / Unattached).

## Steps

1. **Resolve parent story (soft-attach):**
   - If the user names a story (or epic+story) id/title/path, use it.
   - Else infer from prompt + open board context (matching story/epic titles, active story in conversation).
   - Else run `python3 <plugin>/scripts/ensure-general-epic.py <board-root>` and attach under General’s catch-all **Unattached** story.
2. Gather title, description, AC or repro/fix criteria, priority, tags. `type` = `task` or `bug`.
3. Allocate next `T-NNN` or `B-NNN`.
4. Create item file from template under the resolved story’s `items/` (Prompt & feedback, Commits, Work log).
5. Set `parent` = story id, `epic` = ancestor epic id.
6. **Calibrate** per sizing ref: prefer 30-day velocity × points for `estimate_minutes` (else seeds); set `estimate_source` / `estimate_basis`; `effort_minutes: 0`, `actual_minutes: 0`, `session_cap_minutes: 480`.
7. Link from story Tasks; refresh INDEX; roll up story/epic; refresh VELOCITY if useful.
8. Run `sync-taskmark-repos` only if board location / REPOS needs refresh.
9. Reply with id, path, size, points, estimate_minutes, basis, and **assigned story/epic** (including General / Unattached when used).
