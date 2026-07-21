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
3. All child items `done` or `cancelled`, and at least one `done` → `done` (set `completed_at` if unset)
4. Any child `in_progress` or `blocked`, or mix of done + backlog → `in_progress`
5. All children `backlog` or no children → `backlog`

## Epic

Same as story, against child **stories**.

## Start cascade (`started_at`)

When starting a task/bug (or story/epic directly):

1. Set the target’s `started_at` if null (same UTC timestamp as session start).
2. If starting a **task/bug**: also set parent **story** `started_at` if null, then parent **epic** `started_at` if null.
3. If starting a **story**: also set parent **epic** `started_at` if null.
4. Do **not** open Work log sessions on parents unless the user is working the parent itself (avoids double-counting effort).
5. Ancestor status becomes `in_progress` via child rules on sync.

## End cascade (`completed_at`)

When completing a leaf (or after sync-status):

1. Close open Work log sessions on the target with real Ended = now (or idle deadline).
2. Set target `completed_at` if unset when status → `done`.
3. Recompute parent **story**: if all children done/cancelled and ≥1 done → story `done`, set `completed_at` if unset.
4. Recompute parent **epic**: same against stories.
5. Do not invent ≤2 min sessions; do not leave parents `in_progress` when all children are terminal.

## Propagation

After updating an item:

1. Recompute that item’s status (and size rollup for story/epic).
2. Recompute parent story (if task/bug), then parent epic — including start/end timestamp cascades above.
3. Refresh board `INDEX.md`.
4. Bump `updated` on rewritten files.
5. Run `recompute-actuals.py` (optionally `--calibrate`).
