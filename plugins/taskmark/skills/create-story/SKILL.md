---
name: create-story
description: >-
  Create a new Taskmark user story under an epic, allocate S-NNN, suggest t-shirt
  size from history, link from the epic, and update INDEX.md. Use when the user
  asks for a new story or user story on the Taskmark board.
---

# create-story

## Prerequisites

- `taskmark/` initialized; parent epic exists (id or path).
- Read [templates](../taskmark-conventions/references/templates.md), [sizing](../taskmark-conventions/references/sizing.md).

## Steps

1. Resolve parent epic (`E-NNN` or path). Abort with a clear message if missing.
2. Gather title, user story statement, acceptance criteria, priority, tags.
3. Allocate next `S-NNN` by scanning all `story.md` files.
4. Create `taskmark/epics/{epic-folder}/stories/{id}-{slug}/story.md` with empty Tasks, Prompt & feedback, Commits, and Work log tables.
5. Suggest size from done stories (prefer same epic/tags); set `parent` and `epic` to the epic id.
6. Append a Stories link on the parent `epic.md`.
7. Refresh INDEX; optionally run size rollup on the epic via sync-status logic.
8. Propagate board copies with `sync-taskmark-repos` when multiple git roots are in play.
9. Reply with id, path, size, and parent epic.
