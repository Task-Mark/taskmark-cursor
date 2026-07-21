---
name: taskmark-conventions
description: >-
  Canonical Taskmark board conventions for hierarchical epic, story, task, and
  bug markdown under taskmark/. Covers folder layout, frontmatter, templates,
  t-shirt sizing, work logs, prompt/feedback logs, commits logs, multi-repo
  board copies, status derivation, and INDEX. Use when creating or editing
  Taskmark files, answering Taskmark questions, multi-root workspaces, or
  before create-epic, create-story, create-task, start-work, complete-work,
  log-commits, sync-taskmark-repos, commit-all, or sync-status.
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
- [Work log](references/work-log.md)
- [Prompt & feedback log](references/prompt-feedback-log.md)
- [Commits log](references/commits-log.md)
- [Multi-repo boards](references/multi-repo.md)
- [Status derivation](references/status-derivation.md)
- [INDEX format](references/index-format.md)

## Quick rules

- IDs: `E-NNN`, `S-NNN`, `T-NNN`, `B-NNN` (zero-padded, unique board-wide)
- Folder slug: `{id}-{kebab-title}`
- Tasks and bugs live under the story’s `items/`
- Do not hand-set `status` except via `blocked` / `cancelled` latches; run sync-status after changes
- Work log + Commits log on every item; Prompt & feedback on stories, tasks, and bugs
- Multi-root workspaces: every git project gets a full `taskmark/` copy (`sync-taskmark-repos`)
