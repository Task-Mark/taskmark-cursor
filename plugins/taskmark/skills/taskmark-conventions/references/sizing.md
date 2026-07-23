# Sizing, points, and estimates

Seed **estimate** minutes are billable-session oriented (AI-assisted work), not human calendar days. Points stay on the Fibonacci map below. Velocity and calibration use **actual_minutes** (start-work → complete-work sessions).

## T-shirt + story points

| Size | Default points | Default estimate (seed) | Weight |
|------|----------------|-------------------------|--------|
| XS | 1 | 30 min | 1 |
| S | 2 | 2 h (120 min) | 2 |
| M | 3 | 1 day (480 min) | 3 |
| L | 5 | 2 days (960 min) | 4 |
| XL | 8 | 3+ days (1440 min); prefer split | 5 |

Points scale: `1 | 2 | 3 | 5 | 8 | 13`. Use `13` only for manual / high-uncertainty XL.

Also in `SIZING.md`. After enough done items with trustworthy `actual_minutes`, `recompute-actuals.py --calibrate` updates the **Seed estimate** column from median actual per size (≥3 samples; ignores ≤2 min actuals). Labels and points map stay fixed.

## Suggesting on create

Required for `create-task` and `create-story` (recommended for epics):

1. Find `status: done` items of the same `type` (prefer same `tags` / epic).
2. Rank by similarity.
3. **Size:** median t-shirt among top matches (order XS < S < M < L < XL).
4. **Points:** median `points` among top matches; if missing, use size→points map above.
5. **estimate_minutes:** prefer `VELOCITY.md` / script median minutes-per-point over the **rolling 30-day** window (≥3 trustworthy samples with `actual_minutes > 2`): `median(actual/points) × new_points`. Else fall back to SIZING seed table from size.
6. Set `estimate_basis` to e.g. `[velocity:30d:Nmin/pt]` or seed note; `estimate_source: suggested`.
7. Write `size`, `size_source`, `size_basis`, `points`, `points_source`, `estimate_minutes`, `estimate_source`, `actual_minutes: 0`, `session_cap_minutes: 480`.
8. Manual override → `estimate_source: manual` (and optionally `*_source: manual`).

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

## Post-done calibration

After `recompute-actuals.py --calibrate` (from `complete-work` / `sync-status`):

**Per done leaf (task/bug)** with `actual_minutes > 2` and `estimate_minutes > 0`:

- If `actual / estimate` outside `[0.5, 2]`: set `estimate_minutes` toward actual (rounded), note `estimate_basis`; if actual clearly fits another t-shirt vs current seeds, update `size` / `points` with `*_source: suggested`.
- Skip calibration when `actual_minutes ≤ 2`.
- Append a row to `SIZING.md` calibration log.

**Open estimates:** items with `estimate_source` not `manual` may refresh from the latest 30-day median min/point × points.

**Seed table:** median actual per size from done leaves with actual > 2; require ≥3 samples with at least two distinct values (or ≥5 identical) before changing a size row.

## Velocity

Team speed and ETA live in `VELOCITY.md` — use **actual_minutes** over 30 days. See [velocity](velocity.md) and [effort-time](effort-time.md).
