---
name: complete-work
description: >-
  Complete a Taskmark work session: close the Work log (respect session and idle
  caps), log commits and feedback, recompute effort/actual minutes, cascade
  parent completion, sync status, and refresh VELOCITY.md. Use when finishing a
  session or marking delivery.
---

# complete-work

## Prerequisites

Resolve item; read [work-log](../taskmark-conventions/references/work-log.md), [effort-time](../taskmark-conventions/references/effort-time.md), [status-derivation](../taskmark-conventions/references/status-derivation.md).

## Forbidden

- Do **not** invent short closed Work log sessions (especially ≤2 minutes) to “mark done.”
- Do **not** hand-write `effort_minutes` or `actual_minutes`. Always recompute via script.
- Do **not** backfill a fake `Started`/`Ended` pair at session end; close the **real** open session with **now** UTC.

## Steps

1. Find open Work log session. If none, offer sync-status only (still run recompute).
2. Set Ended to **now UTC** (if now is past idle deadline, use idle deadline and note auto-cap). Session caps apply to **effort** only.
3. Update Session Summary with what was accomplished.
4. Align AC / fix criteria checkboxes with reality.
5. Append `feedback` row if the user accepted/rejected or gave final notes.
6. Bump `updated`. Set target `completed_at` if status will be `done` and it is unset.
7. Log commits for touched repos since session start (`log-commits`).
8. **End cascade:** after leaf/story is done, if all siblings are done/cancelled and ≥1 done → set parent story/epic `status: done` and `completed_at` if unset. Walk story → epic.
9. **Recompute (required):** run from the plugin package:
   `python3 scripts/recompute-actuals.py <board-root> --calibrate`
   Writes `effort_minutes` (sessions) and `actual_minutes` (wall-clock), rolls up parents, refreshes INDEX/VELOCITY, calibrates from effort, may refresh open suggested estimates from 30-day velocity.
10. Confirm `completed_at` on target and any cascaded parents.
11. Refresh `REPOS.md` with `sync-taskmark-repos` if multi-repo.
12. Reply with closed session, effort minutes, wall-clock actual, status, and rollups.
