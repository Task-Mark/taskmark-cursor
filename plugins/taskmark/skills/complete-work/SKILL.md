---
name: complete-work
description: >-
  Complete a Taskmark work session: close the Work log (respect session and idle
  caps), ensure a real session exists so Actual is accurate, log commits and
  feedback, cascade parent completion, recompute, and refresh VELOCITY.md.
---

# complete-work

## Prerequisites

Resolve item; read [work-log](../taskmark-conventions/references/work-log.md), [effort-time](../taskmark-conventions/references/effort-time.md), [status-derivation](../taskmark-conventions/references/status-derivation.md).

## Forbidden

- Do **not** mark an item `done` without at least one **closed** Work log session whose billable minutes are **> 2**, **except** shared-batch leaf allocations (batch total > 2; see effort-time).
- Do **not** invent ≤2 minute closed sessions to mark delivery (shared-batch slices that happen to be ≤2 are allowed only as proportional splits of a real batch).
- Do **not** hand-write `actual_minutes`. Always recompute via script.
- Do **not** backfill a fake `Started`/`Ended` pair at session end; close the **real** open session with **now** UTC (or use start-work first if none is open).
- Do **not** copy the same full batch Started/Ended onto every task/story when completing a whole epic in one sitting.

## Steps

1. If there is **no** Work log session (open or closed) on this item, run **start-work** first (or refuse to complete). Every done epic/story/task/bug must have a work log so Actual reflects time spent.
2. Find open Work log session. If none but closed sessions already exist and AC is done, skip to status/cascade (still run recompute).
3. Set Ended to **now UTC** (if now is past idle deadline, use idle deadline and note auto-cap).
4. Update Session Summary with what was accomplished.
5. Align AC / fix criteria checkboxes with reality.
6. Append `feedback` row if the user accepted/rejected or gave final notes.
7. Bump `updated`. Set target `completed_at` if status will be `done` and it is unset.
8. Log commits for touched repos since session start (`log-commits`).
9. **Shared-batch (whole epic/story in one sitting):** if this close finishes a multi-leaf delivery:
   - Let `batch_started` = earliest open/closed session start among the leaves delivered together; `batch_ended` = now (or idle/session cap).
   - Allocate billable minutes across those leaves by **points** (largest-remainder); write each leaf’s Ended as `batch_started + allocated` (same Started). Summaries may include `shared-batch: X of Ymin by points`.
   - Parents get a 0-minute rollup row or no billable session — do not also store the full batch on the parent.
10. **End cascade:** after leaf/story is done, if all siblings are done/cancelled and ≥1 done → set parent story/epic `status: done` and `completed_at` if unset. **Parents that become done must also have a Work log** (0-minute rollup note is OK when children hold the shared-batch split).
11. **Recompute (required):**  
    `python3 scripts/recompute-actuals.py <board-root> --calibrate`  
    Redistributes any remaining identical parallel leaf sessions, writes `actual_minutes`, rolls up parents, refreshes INDEX/VELOCITY.
12. Confirm `completed_at` and that **epic/story Actual ≈ batch wall-clock** (not N × batch) when work was a shared batch.
13. Refresh `REPOS.md` with `sync-taskmark-repos` if multi-repo.
14. Reply with closed session, Actual minutes, status, and rollups.