# Sizing, points (no time estimates)

Suggest **t-shirt size** and **story points** only. Do **not** suggest
`estimate_minutes` from velocity, seeds, or similar (velocity/time-estimate
mechanism removed — board S-057). Keep `estimate_minutes: 0` on create unless
the user sets a manual value later.

Seed **points** map (also in `SIZING.md`):

| Size | Default points | Weight |
|------|----------------|--------|
| XS | 1 | 1 |
| S | 2 | 2 |
| M | 3 | 3 |
| L | 5 | 4 |
| XL | 8 | 5 |

Points scale: `1 | 2 | 3 | 5 | 8 | 13`. Use `13` only for manual / high-uncertainty XL.

## Suggesting on create

Required for `create-task` and `create-story` (recommended for epics' children):

1. Find `status: done` items of the same `type` (prefer same `tags` / epic).
2. Rank by similarity.
3. **Size:** median t-shirt among top matches (order XS < S < M < L < XL).
4. **Points:** median `points` among top matches; if missing, use size→points map above.
5. Set `estimate_minutes: 0`, `estimate_source: suggested`, `estimate_basis: []` (time estimates not suggested).
6. Write `size`, `size_source`, `size_basis`, `points`, `points_source`, `actual_minutes: 0`, `session_cap_minutes: 480`.
7. Manual size/points override → `*_source: manual`.

## Rollups

- Story **points**: **sum of child task/bug `points`** when children exist; else own points.
- Story **size**: from sum of child t-shirt weights (see mapping below) when children exist.
- Story **estimate_minutes**: sum of children when children exist (historical; often 0).
- Story **actual_minutes**: max(sum of children, own work-log billable) when children exist.
- Epic **points**: **sum of child story `points` plus epic-direct task/bug `points`**.
- Epic **size**: **none** (`null`) — epics do not use t-shirt size; only points.
- Epic **estimate_minutes** / **actual_minutes**: sum / max rollup from stories and epic-direct leaves.

Mapping sum of child weights → shirt:

| Sum of weights | Size |
|----------------|------|
| 1 | XS |
| 2–3 | S |
| 4–6 | M |
| 7–10 | L |
| 11+ | XL |

## Calibration

`recompute-actuals.py --calibrate` no longer rewrites open/done time estimates or a
velocity window. It still recomputes actuals and size/points rollups.

## Velocity

Removed. Delivery pace UI is tracked under **E-015 Current Speed** (90-day weekly
points average). Do not create or refresh `VELOCITY.md`.
