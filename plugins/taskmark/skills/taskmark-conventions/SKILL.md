---
name: taskmark-conventions
description: >-
  Canonical Taskmark board conventions for hierarchical epic, story, task, and
  bug markdown under taskmark/. Covers folder layout, frontmatter, templates,
  t-shirt sizing, story points, actual minutes, idle time caps, work logs,
  prompt/feedback, commits, multi-repo copies, status derivation, and INDEX.
  Use when creating or editing Taskmark files, sizing, multi-root workspaces,
  or before create-*, start-work, complete-work, sync-status, log-commits,
  sync-taskmark-repos, commit-all, or sync-plugin-local.
---

# Taskmark conventions

Board root: `taskmark/` inside a single product repo, or the root of a dedicated `<common>-taskmark` git repo in multi-git workspaces (see [folder-layout](references/folder-layout.md), [multi-repo](references/multi-repo.md)).

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
- [Contributor identity](references/identity.md)

## Quick rules

- IDs: `E-NNN`, `S-NNN`, `T-NNN`, `B-NNN` (zero-padded, unique board-wide)
- Folder slug: `{id}-{kebab-title}`
- Tasks and bugs live under a story’s `items/` **or** an epic’s `items/` (no story required)
- Stories and tasks do not require a user-invented parent; prefer contextual attach, else reserved **General** epic
- Do not hand-set `status` except via `blocked` / `cancelled` latches; run sync-status after changes
- Work log + Commits on every item; Prompt & feedback on stories, tasks, and bugs
- Track `size` + `points` + `actual_minutes` (billable sessions); `estimate_minutes` is optional/historical (not suggested by sizing)
- Idle: auto-close open sessions at next-day 12:00 UTC; session_cap_minutes default 480
- Multi-root: sibling `<common>-taskmark` git repo **is** the board root (no nested `taskmark/`); never copy into product repos
