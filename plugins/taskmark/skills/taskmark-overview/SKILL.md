---
name: taskmark-overview
description: >-
  Summarize the Taskmark board from INDEX.md and item frontmatter — by status,
  size, epic, and open work sessions. Use when the user asks what is on the board,
  board status, progress, or an overview of epics, stories, and tasks.
---

# taskmark-overview

## Steps

1. Read `taskmark/INDEX.md` if present; otherwise offer `taskmark-init`.
2. Optionally spot-check open session rows and `in_progress` items’ Work logs for accuracy.
3. Present a concise overview:
   - Counts by status (backlog / in_progress / blocked / done / cancelled)
   - Epics with status and size
   - Open work sessions (item, actor, started)
   - Blocked or cancelled items called out
4. Do not modify files unless the user also asks to sync; if INDEX looks stale vs files, suggest `/sync-status`.
