# Effort and idle time

**Never** use calendar span (`completed_at − started_at`) for effort. A task started in January and finished in May must not count five months.

**Never** hand-set `actual_minutes`. Recompute with `scripts/recompute-actuals.py`.

**Never** invent ≤2 minute closed Work log sessions to mark delivery. Close the real open session with **now** UTC via `complete-work`.

## Billable minutes

`actual_minutes` = sum over Work log sessions of each session’s **billable** minutes (open sessions use **now** as provisional end until closed).

Per session:

1. Let `end_eff` = session `Ended` (or **now** if open; or idle deadline if auto-closed).
2. Let `idle_deadline` = **12:00 UTC on the UTC calendar day after `Started`’s date**.  
   Example: Started `2026-01-01T16:00:00Z` → idle deadline `2026-01-02T12:00:00Z`.
3. Let `cap` = frontmatter `session_cap_minutes` (default **480**).
4. Billable end = `min(end_eff, idle_deadline, Started + cap minutes)`.
5. Billable minutes = `max(0, floor((billable_end − Started) in minutes))`.

## Idle auto-close

When `complete-work`, `sync-status`, `start-work` (before a new session), or the stop hook finds an **open** session (`Ended` is `—`) and **now > idle_deadline**:

1. Set `Ended` to the idle deadline (ISO-8601 UTC).
2. Append to Summary: `auto-closed: idle cap (next-day 12:00 UTC)`.
3. Recompute `actual_minutes` via `recompute-actuals.py`.

If the user `complete-work`s **before** the idle deadline, use the real end time (still apply `session_cap_minutes`).

## Commit-span recovery (only allowed exception)

When Work logs undercount relative to the item’s **Commits** table, `recompute-actuals.py` may insert or extend **one** closed agent session:

- Trigger: ≥2 dated commit rows, **or** 1 commit + `started_at` earlier than that commit; commit span ≥ 10 minutes; work-log billable < 50% of that span.
- Session: Started = first commit (or earlier `started_at`), Ended = last commit; Summary includes `auto-recovered: commit span`.
- Still apply idle deadline and `session_cap_minutes` when billing that session.

Do **not** use pure calendar `completed_at − started_at` as effort. Commit-span recovery is the only automatic fill when logs undercount commits.

## Resume after long gaps

Later work (e.g. May after a January abandoned session) must open a **new** Work log session via `start-work`. Only that new session adds more minutes.

## Story / epic rollup

When children exist: parent `actual_minutes` = **max**(sum of children’s `actual_minutes`, parent’s own work-log billable).  
That preserves epic/story commit-span recovery when leaves undercount.  
Otherwise: parent’s own work-log billable sum.

Always run `scripts/recompute-actuals.py` (optionally `--calibrate`) from `sync-status` / `complete-work` — do not recompute by hand.
