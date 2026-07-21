---
name: taskmark-init
description: >-
  Initialize a Taskmark board by creating taskmark/README.md, INDEX.md, SIZING.md,
  VELOCITY.md, REPOS.md, and an empty epics/ folder. Use when setting up Taskmark
  or when create skills find no taskmark/ root. In multi-root workspaces, follow
  with sync-taskmark-repos.
---

# taskmark-init

## Steps

1. If `taskmark/` already exists with `INDEX.md`, tell the user it is initialized and stop (unless they ask to repair missing files).
2. Create:
   - `taskmark/README.md`
   - `taskmark/INDEX.md` — [index-format](../taskmark-conventions/references/index-format.md) (include Points / Est / Actual columns)
   - `taskmark/SIZING.md` — [sizing](../taskmark-conventions/references/sizing.md)
   - `taskmark/VELOCITY.md` — [velocity](../taskmark-conventions/references/velocity.md) empty template
   - `taskmark/REPOS.md` — [multi-repo](../taskmark-conventions/references/multi-repo.md)
   - `taskmark/epics/` (optional `.gitkeep`)
3. If multiple git roots, run `sync-taskmark-repos`.
4. Confirm paths; point to `/new-epic`.

## Seed INDEX.md

Use headers with Size | Points | Est (min) | Actual (min) and `—` placeholder rows per [index-format](../taskmark-conventions/references/index-format.md).

## Seed VELOCITY.md

```markdown
# Team velocity

Last synced: <now UTC ISO-8601>
Window: last 20 done tasks/bugs (or all if fewer)

## Throughput

| Metric | Value |
|--------|-------|
| Done items in window | 0 |
| Sum points | 0 |
| Median points | — |
| Median actual_minutes | — |
| Median minutes per point | insufficient data |
| Points per week (approx) | insufficient data |

## Remaining backlog

| Metric | Value |
|--------|-------|
| Open items (excl. cancelled) | 0 |
| Sum points remaining | 0 |
| Sum estimate_minutes remaining | 0 |
| ETA (from median min/point) | insufficient data |

## Notes

- Actuals use billable work-log minutes only (idle auto-cap + session cap).
```

## Seed SIZING.md

Include size↔points↔seed estimate table and empty calibration log.
