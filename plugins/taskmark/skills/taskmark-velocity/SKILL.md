---
name: taskmark-velocity
description: >-
  Report Current Speed and delivery ETA from Taskmark done items: 90-day weekly
  points average (excluding current ISO week and zero-point weeks), plus median
  minutes per point for estimate suggestions. Use when the user asks about
  velocity, speed, ETA, or throughput.
---

# taskmark-velocity

## Steps

1. Run `python3 <plugin>/scripts/recompute-actuals.py <board-root>` (prefer `--calibrate` when refreshing open estimates).
2. Read board `VELOCITY.md`.
3. **Current Speed** = average weekly story points of done tasks/bugs over 90 days anchored at the latest completed leaf; exclude the current ISO week and weeks with 0 points.
4. Report remaining open points / estimate_minutes, calendar ETA (`rem_points / Current Speed` weeks), and effort ETA (`median min/pt × rem_points`) when samples exist.
5. Remind: Actual is billable Work log minutes; Est uses median min/pt over the same 90-day window when ≥3 trustworthy samples exist.
