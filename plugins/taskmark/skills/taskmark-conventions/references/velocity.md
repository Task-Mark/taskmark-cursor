# Velocity board file

Path: board root `VELOCITY.md`.

Refreshed by `sync-status`, `complete-work`, and `taskmark-velocity`. Speed uses **actual_minutes** (start-work → complete-work sessions) over a rolling **30-day** window.

```markdown
# Team velocity

Last synced: YYYY-MM-DDTHH:MM:SSZ
Window: rolling 30 days (done tasks/bugs by completed_at)

## Throughput

| Metric | Value |
|--------|-------|
| Done items in window | N |
| Sum points | P |
| Median points | … |
| Median actual_minutes | … |
| Median minutes per point | … |
| Points per week (approx) | … or insufficient data |

## Remaining backlog

| Metric | Value |
|--------|-------|
| Open items (excl. cancelled) | … |
| Sum points remaining | … |
| Sum estimate_minutes remaining | … |
| ETA (from median min/point) | … or insufficient data |

## Notes

- Speed uses **actual_minutes** (start-work → complete-work sessions) over 30 days.
- Est = points × median min/point when ≥3 trustworthy samples exist.
```

## Rules

1. Window = done tasks/bugs with `completed_at` in the last **30 days**.
2. Trustworthy sample: `actual_minutes > 2` and `points > 0`.
3. Median minutes/point = median of `(actual_minutes / points)`. Require **≥3** samples.
4. Create/suggest estimates prefer this median × points; else SIZING seeds.
