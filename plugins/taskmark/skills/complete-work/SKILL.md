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

## Steps

1. Find open Work log session. If none, offer sync-status only.
2. Set Ended to now UTC (if now is past idle deadline, use idle deadline and note auto-cap). Apply billable cap via `session_cap_minutes` when computing actuals.
3. Update Session Summary with what was accomplished.
4. Align AC / fix criteria checkboxes with reality.
5. Append `feedback` row if the user accepted/rejected or gave final notes.
6. Bump `updated`.
7. Log commits for touched repos since session start (`log-commits`).
8. Recompute `actual_minutes`; run sync-status up the tree; set `completed_at` when `done`.
9. If `|actual − estimate|` or size mismatch is stark (>2×), append calibration to `SIZING.md`.
10. Refresh `VELOCITY.md`; propagate with `sync-taskmark-repos` if multi-repo.
11. Reply with closed session, billable minutes added, status, and rollups.
