---
name: taskmark-init
description: >-
  Initialize a Taskmark board (INDEX, SIZING, VELOCITY, REPOS, epics). Single-git:
  under <project>/taskmark/. Multi-git: at sibling <common>-taskmark repo root
  (flat). Use when setting up Taskmark or when create skills find no board.
---

# taskmark-init

## Steps

1. Discover git roots. Decide mode per [multi-repo](../taskmark-conventions/references/multi-repo.md):
   - **One product git root:** target = that root’s `taskmark/`.
   - **Multiple product git roots:** ensure sibling `<common>-taskmark` (ask user if name ambiguous; `git init` if new), target = **that repo’s root** (board files at root — no nested `taskmark/`).
2. If target already has `INDEX.md`, tell the user it is initialized and stop (unless they ask to repair missing files).
3. Create under the target:
   - `README.md`
   - `INDEX.md` — [index-format](../taskmark-conventions/references/index-format.md)
   - `SIZING.md` — [sizing](../taskmark-conventions/references/sizing.md)
   - `VELOCITY.md` — [velocity](../taskmark-conventions/references/velocity.md) empty template
   - `REPOS.md` — [multi-repo](../taskmark-conventions/references/multi-repo.md)
   - `epics/` (optional `.gitkeep`)
4. Run `sync-taskmark-repos` (add `--migrate` when cleaning old per-repo copies or flattening nested boards).
5. Confirm paths; point to `/new-epic`.

## Seed INDEX.md

Use headers with Size | Points | Est (min) | Actual (min) and `—` placeholder rows per [index-format](../taskmark-conventions/references/index-format.md).

## Seed VELOCITY.md

```markdown
# Team velocity

Last synced: <now UTC ISO-8601>
Window: rolling 30 days (done tasks/bugs by completed_at)

## Throughput

| Metric | Value |
|--------|-------|
| Done items in window | 0 |
| Sum points | 0 |
| Median points | — |
| Median effort_minutes | — |
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

- Speed uses **effort_minutes** (session billable) over 30 days; `actual_minutes` is wall-clock lead time.
```

## Seed SIZING.md

Include size↔points↔seed estimate table and empty calibration log.
