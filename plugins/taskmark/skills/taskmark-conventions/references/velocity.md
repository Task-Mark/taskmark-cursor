# Velocity board file

Path: `taskmark/VELOCITY.md`

Refreshed by `sync-status`, `complete-work`, and `taskmark-velocity`. Use **actual_minutes** (idle-capped), never calendar span.

```markdown
# Team velocity

Last synced: YYYY-MM-DDTHH:MM:SSZ
Window: last 20 done tasks/bugs (or all if fewer)

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

- Actuals exclude idle via next-day 12:00 UTC auto-cap and session_cap_minutes.
- ETA = remaining estimate_minutes / recent throughput when enough data exists.
```

## Rules

1. Only **done** tasks/bugs with `points > 0` and `actual_minutes > 0` feed minutes-per-point.
2. Median minutes/point = median of `(actual_minutes / points)` per item in the window.
3. Remaining = non-done, non-cancelled items (tasks/bugs; optionally include stories without children).
4. If fewer than 3 done items with ratios, mark velocity/ETA as **insufficient data**.
