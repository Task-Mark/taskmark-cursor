---
name: create-task
description: >-
  Create a Taskmark task or bug under a story or epic, allocate T-NNN or B-NNN,
  suggest t-shirt size and points from history, link from the parent, and update
  INDEX. Use when the user asks for a new task or bug.
---

# create-task

## Prerequisites

Board exists (else run **full** `taskmark-init`, including `ensure-board-ui.py` / Vercel Node stubs). Read [templates](../taskmark-conventions/references/templates.md), [sizing](../taskmark-conventions/references/sizing.md), [folder-layout](../taskmark-conventions/references/folder-layout.md) (epic-direct items / General).

## Steps

1. **Resolve parent (soft-attach):**
   - If the user names a **story**, use it (`parent` = story, file under that story’s `items/`).
   - Else if the user names an **epic** (or only an epic is clear from context), use it (`parent` = epic, file under that epic’s `items/` — **no story required**).
   - Else infer story or epic from prompt + open board context.
   - Else run `python3 <plugin>/scripts/ensure-general-epic.py <board-root>` and attach under **General**’s epic-level `items/`.
2. Gather title, description, AC or repro/fix criteria, priority, tags. `type` = `task` or `bug`.
3. Allocate next `T-NNN` or `B-NNN`.
4. Create item file from template under the resolved `items/` folder (Prompt & feedback, Commits, Work log).
5. Set frontmatter:
   - Under story: `parent` = story id, `epic` = ancestor epic id.
   - Under epic (no story): `parent` = epic id **and** `epic` = same epic id (never leave `parent: null` — rollups attach via parent/epic).
6. **Size:** suggest t-shirt + points per [sizing](../taskmark-conventions/references/sizing.md). Suggest `estimate_minutes` from Current Speed intensity when available (points × median min/pt over the 90-day window; `estimate_basis: [speed:90d:Nmin/pt]`); else `0`. `actual_minutes: 0`, `session_cap_minutes: 480`.
7. Stamp `reporters` from `scripts/git-identity.py` (merge by email). Upsert README contributors when identity is new.
8. Link from the parent’s Tasks (or epic body list if epic-direct); refresh INDEX; roll up story/epic. **Re-derive parent status** (story and/or epic): a `done` parent with a new open child becomes `in_progress` and clears `completed_at` (epic status includes epic-direct leaves — see status-derivation).
9. Run `sync-taskmark-repos` only if board location / REPOS needs refresh.
10. Reply with id, path, size, points, and **assigned parent** (story and/or epic, including General when used).
