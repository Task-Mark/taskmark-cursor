---
name: start-work
description: >-
  Start work on a Taskmark epic, story, task, or bug: append a prompt summary to
  the Prompt & feedback log (stories/tasks/bugs), open a Work log session with
  actor and start time, set started_at if needed, and sync status. Use when the
  user or agent begins implementing or actively working on a board item.
---

# start-work

## Prerequisites

- Resolve item by id (`E-`/`S-`/`T-`/`B-`) or file path.
- Read [work-log](../taskmark-conventions/references/work-log.md), [prompt-feedback-log](../taskmark-conventions/references/prompt-feedback-log.md), [status-derivation](../taskmark-conventions/references/status-derivation.md).

## Steps

1. Locate the item markdown file under `taskmark/`.
2. **Prompt & feedback** (story / task / bug only): append a `prompt` row summarizing the current user request (faithful summary, not full transcript). Skip if this turn has no user prompt (e.g. pure `/start-work` with no new ask — still note “User invoked start-work on {id}” only if useful; prefer summarizing the linked request).
3. **Work log**: if an open session already exists (Ended `—`), do not open another; tell the user and reuse it. Otherwise append the next session row:
   - Actor: `agent` when the AI is doing the work; `user` when the human is; default `agent` for agent-driven implementation
   - Started: now UTC ISO-8601
   - Ended: `—`
   - Summary: short “In progress: …” note
4. If `started_at` is null, set it to the session start time.
5. Bump `updated`.
6. Run the same derivation as `sync-status` for this item and ancestors; refresh INDEX.
7. If the workspace has multiple git roots, ensure boards are synced (`sync-taskmark-repos`) before coding across repos.
8. Confirm item id, session number, and new status.

## Actor choice

- Product implementation by the agent → `agent`
- User says they are working manually → `user`
