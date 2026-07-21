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

## Forbidden

- Do **not** hand-set `actual_minutes` or invent ≤2 minute closed sessions.
- Do **not** recompute actuals by mental math — always run the script.

## Steps

1. Resolve starting item or sync the **entire board**.
2. **Idle auto-close:** for every open Work log session past idle deadline (12:00 UTC next day after Started), set Ended to that deadline, append `auto-closed: idle cap (next-day 12:00 UTC)` to Summary.
3. **Recompute (required):** run
   `python3 <plugin>/scripts/recompute-actuals.py <project>/taskmark --calibrate`
   This:
   - applies commit-span recovery when work-log billable ≪ commit span
   - writes leaf `actual_minutes` from billable sessions
   - rolls up story/epic size, points, estimate, actual (actual = max(sum children, own sessions))
   - calibrates mismatched done estimates / SIZING seeds
   - refreshes `INDEX.md` and `VELOCITY.md`
4. For each item, derive `status` from AC / children / latches; set `completed_at` when entering `done`.
5. Report changes (status, actual_minutes, idle closes, recoveries, calibrations).

## Full board sync

Idle-close → `recompute-actuals.py --calibrate` → status derivation → report.
