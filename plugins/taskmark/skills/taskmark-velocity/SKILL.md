---
name: taskmark-velocity
description: >-
  Report team velocity and delivery ETA from Taskmark done items: median minutes
  per story point, remaining points and estimates, using idle-capped actual_minutes.
  Use when the user asks about velocity, speed, ETA, or throughput.
---

# taskmark-velocity

## Prerequisites

Read [velocity](../taskmark-conventions/references/velocity.md), [effort-time](../taskmark-conventions/references/effort-time.md), [sizing](../taskmark-conventions/references/sizing.md).

## Steps

1. Prefer refreshing via sync-status logic (idle-close + recompute actuals) then rewrite `taskmark/VELOCITY.md`.
2. Scan done tasks/bugs (last 20): points, actual_minutes, minutes/point ratios.
3. Scan remaining non-cancelled items: sum points, sum estimate_minutes.
4. Report Throughput + Remaining + ETA tables.
5. Remind: actuals are billable sessions only (next-day 12:00 UTC idle cap + session_cap); never calendar span.
6. If fewer than 3 done ratios, say **insufficient data** for stable velocity/ETA.
