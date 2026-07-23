---
name: start-work
description: >-
  Start work on a Taskmark item: idle-close any stale open session, append a
  prompt summary, open a new Work log session, cascade started_at to parents,
  sync status. Use when the user or agent begins implementing a board item.
---

# start-work

## Prerequisites

Resolve item; read [work-log](../taskmark-conventions/references/work-log.md), [effort-time](../taskmark-conventions/references/effort-time.md), [status-derivation](../taskmark-conventions/references/status-derivation.md), [prompt-feedback-log](../taskmark-conventions/references/prompt-feedback-log.md).

## Forbidden

- Open **one** real session with Started = **now UTC** and Ended = `—` on the **target** item only.
- Do **not** invent closed sessions (especially ≤2 minutes) at start or later to backfill delivery.
- Do **not** hand-set `effort_minutes` or `actual_minutes`.
- Do **not** open Work log sessions on parent story/epic just for cascade (avoids double-counting effort).
- When the user asks to implement a **whole epic** (or many leaves) in one sitting, prefer **one** open session on the epic or the first leaf, then on complete-work **split** minutes across delivered leaves by points (see complete-work shared-batch / effort-time). Do not open the same full-span session on every task up front.
## Steps

1. Locate the item markdown under the board root.
2. **Idle auto-close:** if an open session exists and now > idle deadline, close it at the deadline with Summary note `auto-closed: idle cap (next-day 12:00 UTC)`, then run `recompute-actuals.py` (or sync-status).
3. If an open session still exists (within idle window), do not open another — reuse it and tell the user.
4. **Prompt & feedback** (story/task/bug): append a `prompt` row for the current user request; set **Author** from `scripts/git-identity.py` name when available.
5. Append next Work log session on the **target**: Actor = git `user.name` when available (else `agent` or `user`), Started=now UTC, Ended=`—`, Summary “In progress: …”.
6. Set target `started_at` if null (same timestamp).
7. **Start cascade:**
   - Task/bug → if parent is a story and `started_at` is null, set it; then if epic exists and `started_at` is null, set it. If parent is an epic (epic-direct leaf), only cascade to that epic. Skip missing parents.
   - Story → if epic exists and `started_at` is null, set it.
   - Epic → only own `started_at`.
8. Bump `updated` on edited files; set ancestors to `in_progress` via sync.
9. Sync status for item + ancestors (`sync-status` / recompute script); refresh INDEX.
10. Multi-repo: `sync-taskmark-repos` if `REPOS.md` / board location needs refresh.
11. Confirm id, session number, status, cascaded parents, and any idle auto-close.
