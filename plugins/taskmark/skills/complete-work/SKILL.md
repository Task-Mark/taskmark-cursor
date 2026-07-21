---
name: complete-work
description: >-
  Complete a work session on a Taskmark item: close the open Work log row,
  log related git commits, optionally record user feedback, align acceptance
  criteria, sync derived status, and propagate the board across multi-repo
  copies. Use when finishing a session, marking delivery, or closing agent work.
---

# complete-work

## Prerequisites

- Resolve item id/path; read work-log and status-derivation references.

## Steps

1. Find the open Work log session (Ended is `—` or empty). If none, report and stop (or offer to sync-status only).
2. Set Ended to now UTC; update Session Summary with what was accomplished.
3. Acceptance / fix criteria: tick boxes that are truly done; do not mark done criteria the user did not confirm if ambiguous — ask briefly.
4. **Prompt & feedback** (story/task/bug): if the user accepted, rejected, or gave final notes this turn, append a `feedback` row.
5. Bump `updated`.
6. **Commits**: for each git root touched this session, collect commits since the open session’s Started time and append rows to the item’s Commits table (follow `log-commits`). Optionally mirror notable SHAs onto the parent story/epic.
7. Run sync-status derivation for item → story → epic; set `completed_at` when status becomes `done`.
8. If size vs actual duration clearly mismatched, append a calibration line to `taskmark/SIZING.md`.
9. Propagate board with `sync-taskmark-repos` when multiple git roots are linked.
10. Reply with closed session, commits logged, status, and parent rollup changes.
