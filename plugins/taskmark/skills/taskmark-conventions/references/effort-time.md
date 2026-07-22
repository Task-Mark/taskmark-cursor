# Effort and idle time

Taskmark shows **two** time columns:

| Field | Meaning |
|-------|---------|
| `estimate_minutes` (**Est**) | Planned time = points × 30-day median min/point (else SIZING seed). |
| `actual_ms` | Precise billable Work log duration in **milliseconds** (script-derived). |
| `actual_minutes` (**Actual**, velocity) | `floor(actual_ms / 60000)` — used for velocity and Est calibration. |

**Never** use calendar span (`completed_at − started_at`) for Actual. Overnight gaps must not inflate time spent.

**Never** hand-set `actual_minutes` or `actual_ms`. Recompute with `scripts/recompute-actuals.py`.

**Never** invent ≤2 minute closed Work log sessions to mark delivery. Close the real open session with **now** UTC via `complete-work`.

**Done ⇒ work log:** every `done` epic/story/task/bug must have Work log session(s) totaling **> 2** billable minutes. If completing without a session, run `start-work` first. Historical gaps may be backfilled with a closed session of `points × 30-day median min/point` (see [velocity](velocity.md)), never a ≤2 minute stub.

## Billable minutes (Actual)

`actual_ms` = sum over Work log sessions of each session’s **billable** milliseconds (open sessions use **now** as provisional end until closed). `actual_minutes` = `floor(actual_ms / 60000)`.

Per session:

1. Let `end_eff` = session `Ended` (or **now** if open; or idle deadline if auto-closed).
2. Let `idle_deadline` = **12:00 UTC on the UTC calendar day after `Started`’s date**.
3. Let `cap` = frontmatter `session_cap_minutes` (default **480**).
4. Billable end = `min(end_eff, idle_deadline, Started + cap minutes)`.
5. Billable ms = `max(0, floor((billable_end − Started) in milliseconds))`.
6. Allocate shared-batch slices in **ms** (same Started; Ended = Started + allocated ms). Summaries may note `shared-batch: X of Yms by points`.

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

- Parent `actual_ms` = **max**(sum of children’s `actual_ms`, parent’s own work-log billable ms).
- Parent `actual_minutes` = `floor(actual_ms / 60000)`.
- Parent `estimate_minutes` / `points` / `size` = child rollups as in [sizing](sizing.md).

`started_at` / `completed_at` still cascade for status (start/end work) but do **not** define Actual.

## Shared-batch delivery (implement whole epic/story in one sitting)

When one wall-clock session delivers **multiple** leaves:

1. Measure **one** batch span: `batch_started` → `batch_ended` (billable after idle/session caps).
2. **Never** copy that full Started/Ended onto every leaf (that makes Actual ≈ N × batch).
3. Allocate **milliseconds** by **points** (fallback `estimate_minutes`) with largest-remainder so allocations **sum exactly** to the batch billable total.
4. On each leaf, write a closed Work log row with the **same** `Started` = `batch_started` and `Ended` = `Started + allocated_ms` (not the full batch end). Summary may note `shared-batch: X of Yms by points`.
5. Parents (story/epic): either omit a billable session or record a **0-minute** rollup row; Actual comes from child sum (= batch total).
6. Leaf billable may be **≤ 2** when the batch total is **> 2** and the row is a shared-batch allocation. Do not invent extra minutes to satisfy the usual >2 rule on every leaf.
7. `recompute-actuals.py` also **detects** identical closed (Started, Ended) leaf sessions under an epic and redistributes the same way (repairs historical inflation).

Always run `scripts/recompute-actuals.py` (optionally `--calibrate`) from `sync-status` / `complete-work`.
