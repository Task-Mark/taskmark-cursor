---
name: sync-status
description: >-
  Idle-close stale Taskmark work sessions, recompute status, size/points rollups,
  actual_minutes from billable sessions, refresh INDEX.md and VELOCITY.md. Use
  after AC edits, work-log changes, or when the user asks to sync board status.
---

# sync-status

## Prerequisites

Read [status-derivation](../taskmark-conventions/references/status-derivation.md), [effort-time](../taskmark-conventions/references/effort-time.md), [sizing](../taskmark-conventions/references/sizing.md), [velocity](../taskmark-conventions/references/velocity.md), [index-format](../taskmark-conventions/references/index-format.md).

## Steps

1. Resolve starting item or sync the **entire board**.
2. **Idle auto-close:** for every open Work log session past idle deadline (12:00 UTC next day after Started), set Ended to that deadline, append `auto-closed: idle cap (next-day 12:00 UTC)` to Summary.
3. For each task/bug: recompute `actual_minutes` from billable sessions ([effort-time](../taskmark-conventions/references/effort-time.md)); derive `status`; set `completed_at` when entering `done`.
4. For each story: roll up child status, `size`, `points` (sum), `estimate_minutes` (sum), `actual_minutes` (sum of children).
5. For each epic: same against child stories.
6. Rewrite `taskmark/INDEX.md` (include Points / Est / Actual columns).
7. Rewrite `taskmark/VELOCITY.md` from done tasks/bugs (last 20) + remaining backlog.
8. Report changes (status, actual_minutes, idle closes).

## Full board sync

Leaves (items) first → stories → epics → INDEX → VELOCITY.
