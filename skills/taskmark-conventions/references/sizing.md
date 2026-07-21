# Sizing (t-shirt)

Scale (also in `taskmark/SIZING.md`):

| Size | Meaning | Rough effort signal | Weight |
|------|---------|---------------------|--------|
| XS | Trivial | Minutes; one-liner / config | 1 |
| S | Small | Under ~half day | 2 |
| M | Medium | About a day | 3 |
| L | Large | Multi-day | 4 |
| XL | Extra large | Split if possible | 5 |

## Suggesting size on create

Required for `create-task` and `create-story` (and recommended for epics):

1. Find `status: done` items of the same `type` (prefer same `tags` and same epic).
2. Rank by similarity (tag overlap, title/description keywords, same epic).
3. Take the **median** size among top matches (order: XS < S < M < L < XL).
4. If fewer than 3 matches, use `M` for stories/tasks (or best judgment from `SIZING.md`) and note low confidence in the create reply.
5. Write `size`, `size_source: suggested`, `size_basis: [ids…]`.
6. Manual override → `size_source: manual` (keep or clear basis for audit).

## Rollups

- Story size = t-shirt mapped from **sum of child task/bug weights**.
- Epic size = same from child story sizes (use each story’s current `size` weight).

Mapping sum → shirt (tasks under a story):

| Sum of weights | Size |
|----------------|------|
| 1 | XS |
| 2–3 | S |
| 4–6 | M |
| 7–10 | L |
| 11+ | XL |

If a story has no children, keep its suggested/manual size.

After an item is `done`, if work-log duration clearly disagrees with `size`, append one line to `taskmark/SIZING.md` calibration log.
