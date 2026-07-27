# Sizing, points, and suggested estimates

Suggest **t-shirt size**, **story points**, and (when speed samples exist)
**estimate_minutes** from Current Speed intensity. See [velocity](velocity.md).

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
5. **Est:** if `VELOCITY.md` / recompute reports median min/point for the 90-day window, set `estimate_minutes = round5(points × median)`; `estimate_basis: [speed:90d:Nmin/pt]`; `estimate_source: suggested`. If insufficient samples, use `estimate_minutes: 0` and `estimate_basis: []`.
6. Write `size`, `size_source`, `size_basis`, `points`, `points_source`, `actual_minutes: 0`, `session_cap_minutes: 480`.
7. Manual size/points/estimate override → `*_source: manual`.

## Rollups

- Story **points**: **sum of child task/bug `points`** when children exist; else own points.
- Story **size**: from sum of child t-shirt weights (see mapping below) when children exist.
- Story **estimate_minutes**: sum of children when children exist.
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

`recompute-actuals.py --calibrate` refreshes non-manual open leaf estimates from the
90-day median min/point, may recalibrate wildly off done estimates, updates
`SIZING.md` seed medians when enough samples exist, and always refreshes
`VELOCITY.md` / `INDEX.md`.

## Velocity

Board `VELOCITY.md` reports **Current Speed** (90-day weekly points average —
same rule as E-015 UI) plus median min/point and ETA. Refresh via recompute /
`taskmark-velocity`.
