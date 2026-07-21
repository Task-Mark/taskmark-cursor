# Sizing, points, and estimates

## T-shirt + story points

| Size | Default points | Default estimate (seed) | Weight |
|------|----------------|-------------------------|--------|
| XS | 1 | 30 min | 1 |
| S | 2 | 2 h (120 min) | 2 |
| M | 3 | 1 day (480 min) | 3 |
| L | 5 | 2 days (960 min) | 4 |
| XL | 8 | 3+ days (1440 min); prefer split | 5 |

Points scale: `1 | 2 | 3 | 5 | 8 | 13`. Use `13` only for manual / high-uncertainty XL.

Also in `taskmark/SIZING.md`.

## Suggesting on create

Required for `create-task` and `create-story` (recommended for epics):

1. Find `status: done` items of the same `type` (prefer same `tags` / epic).
2. Rank by similarity.
3. **Size:** median t-shirt among top matches (order XS < S < M < L < XL).
4. **Points:** median `points` among top matches; if missing, use size→points map above.
5. **estimate_minutes:** if ≥3 done items have both `actual_minutes` and `points` > 0, use `median(actual_minutes / points) × new_points`; else seed table from size.
6. Write `size`, `size_source`, `size_basis`, `points`, `points_source`, `estimate_minutes`, `estimate_basis`, `actual_minutes: 0`, `session_cap_minutes: 480`.
7. Manual override → `*_source: manual`.

## Rollups

- Story/epic **size**: from sum of child t-shirt weights (see mapping below).
- Story/epic **points**: sum of child `points` when children exist; else own points.
- Story/epic **estimate_minutes** / **actual_minutes**: sum of children when children exist.

Mapping sum of child weights → shirt:

| Sum of weights | Size |
|----------------|------|
| 1 | XS |
| 2–3 | S |
| 4–6 | M |
| 7–10 | L |
| 11+ | XL |

After an item is `done`, if `actual_minutes` clearly disagrees with `estimate_minutes` or `size` (e.g. >2×), append a calibration line to `taskmark/SIZING.md`.

## Velocity

Team speed and ETA live in `taskmark/VELOCITY.md` — use **actual_minutes** (idle-capped), never calendar span. See [effort-time](effort-time.md).
