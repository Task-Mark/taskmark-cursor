# Status derivation

Never hand-edit `status` except by setting `blocked: true` or `cancelled: true` (or clearing them). Always run sync-status after AC, work-log, or child changes.

## Task / bug

Evaluate in order:

1. `cancelled: true` → `cancelled`
2. `blocked: true` → `blocked`
3. All acceptance / fix criteria checkboxes checked **and** no open work session → `done` (set `completed_at` if unset)
4. Open work session **or** any criterion checked (but not all) **or** `started_at` set → `in_progress`
5. Else → `backlog`

Open work session = a Work log row with empty or `—` Ended.

## Story

1. `cancelled: true` → `cancelled`
2. `blocked: true` → `blocked`
3. All child items `done` or `cancelled`, and at least one `done` → `done`
4. Any child `in_progress` or `blocked`, or mix of done + backlog → `in_progress`
5. All children `backlog` or no children → `backlog`

## Epic

Same as story, against child **stories**.

## Propagation

After updating an item:

1. Recompute that item’s status (and size rollup for story/epic).
2. Recompute parent story (if task/bug), then parent epic.
3. Refresh `taskmark/INDEX.md`.
4. Bump `updated` on rewritten files.
