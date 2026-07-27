---
name: sync-status
description: >-
  Idle-close stale Taskmark work sessions, recompute status, size/points rollups,
  effort_minutes and wall-clock actual_minutes, refresh INDEX.md.
  Use after AC edits, work-log changes, or when the user asks to sync board status.
---

# sync-status

## Prerequisites

Read [status-derivation](../taskmark-conventions/references/status-derivation.md), [effort-time](../taskmark-conventions/references/effort-time.md), [sizing](../taskmark-conventions/references/sizing.md), [index-format](../taskmark-conventions/references/index-format.md).

## Forbidden

- Do **not** hand-set `effort_minutes` or `actual_minutes` or invent ≤2 minute closed sessions.
- Do **not** recompute by mental math — always run the script.

## Steps

1. Resolve starting item or sync the **entire board**.
2. **Idle auto-close:** for every open Work log session past idle deadline (12:00 UTC next day after Started), set Ended to that deadline, append `auto-closed: idle cap (next-day 12:00 UTC)` to Summary.
3. For each item, derive `status` from AC / children / latches; apply **end cascade** (last child done → parent done + `completed_at`); set `completed_at` when entering `done`.
4. **Recompute (required):** run
   `python3 <plugin>/scripts/recompute-actuals.py <board-root> --calibrate`
   This:
   - redistributes identical parallel leaf Work log spans (shared-batch) by points
   - applies commit-span recovery into **effort** when work-log billable ≪ commit span
   - recovers missing `started_at` from first work-log session when done
   - writes `actual_minutes` / `actual_ms` from billable sessions
   - rolls up story/epic size, points, estimate (historical), actual
   - does **not** refresh velocity or suggest time estimates (removed — S-057)
   - refreshes `INDEX.md`
5. Report changes (status, effort, actual, idle closes, recoveries, cascades).

## Full board sync

Idle-close → status + end cascade → `recompute-actuals.py --calibrate` → report.
