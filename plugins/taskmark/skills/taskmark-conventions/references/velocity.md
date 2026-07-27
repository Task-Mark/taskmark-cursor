# Velocity board file

Path: board root `VELOCITY.md`.

Refreshed by `sync-status`, `complete-work`, and `taskmark-velocity` via `recompute-actuals.py`.

**Current Speed** matches the board UI (E-015): average weekly story points of done tasks/bugs over a **90-day** window anchored at the latest completed leaf. Exclude the **current** ISO week and weeks with **0** points.

```markdown
# Team velocity

Last synced: YYYY-MM-DDTHH:MM:SSZ
Window: Current Speed 90-day weekly points average (done tasks/bugs by completed_at)

## Throughput

| Metric | Value |
|--------|-------|
| Current Speed (pts/week) | … |
| Active weeks in average | … |
| Done items in window | N |
| Sum points in window | P |
| Median points | … |
| Median actual_minutes | … |
| Median minutes per point | … |

## Remaining backlog

| Metric | Value |
|--------|-------|
| Open items (excl. cancelled) | … |
| Sum points remaining | … |
| Sum estimate_minutes remaining | … |
| ETA (calendar weeks @ Current Speed) | … |
| ETA (from median min/point) | … |
```

## Rules

1. Window anchor = max `completed_at` among done tasks/bugs; look back **90 days**.
2. Current Speed = mean of weekly point totals after excluding current ISO week and zero-point weeks.
3. Trustworthy intensity sample: `actual_minutes > 2` and `points > 0` in that window. Median min/point requires **≥3** samples.
4. Create/suggest estimates prefer median × points (`estimate_basis: [speed:90d:Nmin/pt]`); else leave `0` until enough samples exist.
