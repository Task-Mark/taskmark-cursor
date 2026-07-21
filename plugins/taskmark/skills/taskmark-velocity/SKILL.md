---
name: taskmark-velocity
description: >-
  Report team velocity and delivery ETA from Taskmark done items: median minutes
  per story point over a rolling 30-day window (effort_minutes), remaining points
  and estimates. Use when the user asks about velocity, speed, ETA, or throughput.
---

# taskmark-velocity

## Steps

1. Run or read board `VELOCITY.md` (prefer `recompute-actuals.py` first).
2. Window = done tasks/bugs with `completed_at` in the last **30 days**.
3. Median min/point from trustworthy `effort_minutes / points` (≥3 samples, effort > 2).
4. Report remaining open points / estimate_minutes and ETA = median × remaining points when available.
5. Remind: velocity uses **effort_minutes** (session billable); `actual_minutes` is wall-clock lead time.
