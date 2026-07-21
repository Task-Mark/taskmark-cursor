---
name: taskmark-conventions
description: >-
  Canonical Taskmark board conventions for hierarchical epic, story, task, and
  bug markdown under taskmark/. Covers folder layout, frontmatter, templates,
  t-shirt sizing, story points, estimate/actual minutes, idle time caps, work
  logs, prompt/feedback, commits, multi-repo copies, velocity, status derivation,
  and INDEX. Use when creating or editing Taskmark files, sizing, velocity, ETA,
  multi-root workspaces, or before create-*, start-work, complete-work,
  sync-status, log-commits, sync-taskmark-repos, commit-all, taskmark-velocity,
  or sync-plugin-local.
---

# Taskmark conventions

Board root: `taskmark/` at the project root.

## Before writing any board file

1. Read the relevant reference below.
2. Follow ID, folder, frontmatter, and section rules exactly.
3. Never invent a parallel todo system outside `taskmark/`.

## References

- [Folder layout](references/folder-layout.md)
- [Frontmatter](references/frontmatter.md)
- [Templates](references/templates.md)
- [Sizing](references/sizing.md)
- [Points and time](references/points-and-time.md)
- [Effort and idle time](references/effort-time.md)
- [Work log](references/work-log.md)
- [Prompt & feedback log](references/prompt-feedback-log.md)
- [Commits log](references/commits-log.md)
- [Multi-repo boards](references/multi-repo.md)
- [Status derivation](references/status-derivation.md)
- [INDEX format](references/index-format.md)
- [Velocity](references/velocity.md)

## Quick rules

- IDs: `E-NNN`, `S-NNN`, `T-NNN`, `B-NNN` (zero-padded, unique board-wide)
- Folder slug: `{id}-{kebab-title}`
- Tasks and bugs live under the story’s `items/`
- Do not hand-set `status` except via `blocked` / `cancelled` latches; run sync-status after changes
- Work log + Commits on every item; Prompt & feedback on stories, tasks, and bugs
- Track `size` + `points` + `estimate_minutes` + `actual_minutes` (billable sessions only — never calendar span)
- Idle: auto-close open sessions at next-day 12:00 UTC; session_cap_minutes default 480
- Multi-root: every git project gets a full `taskmark/` copy (`sync-taskmark-repos`)
