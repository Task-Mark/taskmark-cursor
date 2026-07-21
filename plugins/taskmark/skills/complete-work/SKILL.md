---
name: complete-work
description: >-
  Complete a Taskmark work session: close the Work log (respect session and idle
  caps), log commits and feedback, recompute actual_minutes, sync status, and
  refresh VELOCITY.md. Use when finishing a session or marking delivery.
---

# complete-work

## Prerequisites

Resolve item; read [work-log](../taskmark-conventions/references/work-log.md), [effort-time](../taskmark-conventions/references/effort-time.md), [status-derivation](../taskmark-conventions/references/status-derivation.md).

## Forbidden

- Do **not** invent short closed Work log sessions (especially ≤2 minutes) to “mark done.”
- Do **not** hand-write `actual_minutes`. Always recompute via script.
- Do **not** backfill a fake `Started`/`Ended` pair at session end; close the **real** open session with **now** UTC.

## Steps

1. Find open Work log session. If none, offer sync-status only (still run recompute).
2. Set Ended to **now UTC** (if now is past idle deadline, use idle deadline and note auto-cap). Apply billable cap via `session_cap_minutes` when computing actuals.
3. Update Session Summary with what was accomplished.
4. Align AC / fix criteria checkboxes with reality.
5. Append `feedback` row if the user accepted/rejected or gave final notes.
6. Bump `updated`.
7. Log commits for touched repos since session start (`log-commits`).
8. **Recompute actuals (required):** run from the plugin package:
   `python3 scripts/recompute-actuals.py <project>/taskmark --calibrate`
   (or `scripts/recompute-actuals.sh`). This closes commit-span undercounts, writes leaf `actual_minutes`, rolls up parents, refreshes INDEX/VELOCITY, and calibrates estimates/SIZING when `|actual/estimate|` is outside `[0.5, 2]`.
9. Confirm `completed_at` when status is `done` after sync.
10. Propagate with `sync-taskmark-repos` if multi-repo.
11. Reply with closed session, billable minutes added, status, and rollups.
