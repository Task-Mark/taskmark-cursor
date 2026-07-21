# Effort and idle time

Taskmark shows **two** time columns:

| Field | Meaning |
|-------|---------|
| `estimate_minutes` (**Est**) | Planned time = points × 30-day median min/point (else SIZING seed). |
| `actual_minutes` (**Actual**) | Time spent = billable Work log sessions opened by **start-work** and closed by **complete-work**. |

**Never** use calendar span (`completed_at − started_at`) for Actual. Overnight gaps must not inflate time spent.

**Never** hand-set `actual_minutes`. Recompute with `scripts/recompute-actuals.py`.

**Never** invent ≤2 minute closed Work log sessions to mark delivery. Close the real open session with **now** UTC via `complete-work`.

## Billable minutes (Actual)

`actual_minutes` = sum over Work log sessions of each session’s **billable** minutes (open sessions use **now** as provisional end until closed).

Per session:

1. Let `end_eff` = session `Ended` (or **now** if open; or idle deadline if auto-closed).
2. Let `idle_deadline` = **12:00 UTC on the UTC calendar day after `Started`’s date**.
3. Let `cap` = frontmatter `session_cap_minutes` (default **480**).
4. Billable end = `min(end_eff, idle_deadline, Started + cap minutes)`.
5. Billable minutes = `max(0, floor((billable_end − Started) in minutes))`.

## Estimates (Est)

On create (and when refreshing suggested estimates): `estimate_minutes = points × median(actual/points)` over done tasks/bugs with `completed_at` in the last **30 days** and `actual_minutes > 2`. If fewer than 3 samples, use the SIZING seed for the t-shirt size. Record `estimate_basis` as `[velocity:30d:Nmin/pt]` or seed.

## Idle auto-close

When `complete-work`, `sync-status`, `start-work` (before a new session), or the stop hook finds an **open** session (`Ended` is `—`) and **now > idle_deadline**:

1. Set `Ended` to the idle deadline (ISO-8601 UTC).
2. Append to Summary: `auto-closed: idle cap (next-day 12:00 UTC)`.
3. Recompute via `recompute-actuals.py`.

## Commit-span recovery

When Work logs undercount relative to the item’s **Commits** table, `recompute-actuals.py` may insert or extend **one** closed agent session (still idle- and session-capped). That feeds **Actual** only.

## Story / epic rollup

When children exist:

- Parent `actual_minutes` = **max**(sum of children’s `actual_minutes`, parent’s own work-log billable).
- Parent `estimate_minutes` / `points` / `size` = child rollups as in [sizing](sizing.md).

`started_at` / `completed_at` still cascade for status (start/end work) but do **not** define Actual.

Always run `scripts/recompute-actuals.py` (optionally `--calibrate`) from `sync-status` / `complete-work`.
