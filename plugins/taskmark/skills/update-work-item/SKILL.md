---
name: update-work-item
description: >-
  Update Taskmark item fields such as title, priority, tags, owner, blocked or
  cancelled latches, or manual size override, then run status sync. Use when the
  user asks to edit, rename, block, unblock, cancel, or re-prioritize a board item
  without starting a full work session.
---

# update-work-item

## Allowed edits

| Field | Notes |
|-------|--------|
| `title` | Update H1 to match; optionally rename folder/file slug if safe and user agrees |
| `priority` | critical / high / medium / low |
| `tags` | Replace or merge as requested |
| `owner` | String |
| `blocked` / `cancelled` | Latches — then sync-status |
| `size` | Set `size_source: manual`; keep or clear `size_basis` |
| `points` | Set `points_source: manual` |
| `estimate_minutes` | Manual plan override; set `estimate_basis` as needed |
| `session_cap_minutes` | Max billable minutes per session (default 480) |
| Body sections | Goal, AC, notes, etc. |

## Do not

- Hand-set `status` directly (use latches + sync)
- Set `effort_minutes` or `actual_minutes` by hand — always recompute via sync
- Delete work-log or prompt/feedback history rows

## Steps

1. Resolve item; apply requested edits; bump `updated`.
2. If title/path rename, update parent link lists and INDEX paths.
3. Run sync-status for the item and ancestors (refreshes actuals / INDEX).
4. Confirm diff of changed fields.
