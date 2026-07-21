---
name: start-work
description: >-
  Start work on a Taskmark item: idle-close any stale open session, append a
  prompt summary, open a new Work log session, sync status. Use when the user or
  agent begins implementing a board item.
---

# start-work

## Prerequisites

Resolve item; read [work-log](../taskmark-conventions/references/work-log.md), [effort-time](../taskmark-conventions/references/effort-time.md), [prompt-feedback-log](../taskmark-conventions/references/prompt-feedback-log.md).

## Forbidden

- Open **one** real session with Started = **now UTC** and Ended = `—`.
- Do **not** invent closed sessions (especially ≤2 minutes) at start or later to backfill delivery.
- Do **not** hand-set `actual_minutes`.

## Steps

1. Locate the item markdown under `taskmark/`.
2. **Idle auto-close:** if an open session exists and now > idle deadline, close it at the deadline with Summary note `auto-closed: idle cap (next-day 12:00 UTC)`, then run `recompute-actuals.py` (or sync-status).
3. If an open session still exists (within idle window), do not open another — reuse it and tell the user.
4. **Prompt & feedback** (story/task/bug): append a `prompt` row for the current user request.
5. Append next Work log session: Actor `agent` or `user`, Started=now UTC, Ended=`—`, Summary “In progress: …”.
6. Set `started_at` if null; bump `updated`.
7. Sync status for item + ancestors (`sync-status` / recompute script); refresh INDEX.
8. Multi-repo: `sync-taskmark-repos` if needed.
9. Confirm id, session number, status, and any idle auto-close.
