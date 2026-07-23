# INDEX format

Path: `taskmark/INDEX.md`

Maintain this file on every create, status sync, or meaningful board change.

```markdown
# Board index

Last synced: YYYY-MM-DDTHH:MM:SSZ

## Epics

| ID | Title | Status | Size | Points | Est (min) | Actual (min) | Path |
|----|-------|--------|------|--------|-----------|--------------|------|
| E-001 | User authentication | in_progress | — | 13 | 960 | 225 | [epic.md](epics/E-001-user-auth/epic.md) |

## Stories

| ID | Title | Epic | Status | Size | Points | Est (min) | Actual (min) | Path |
|----|-------|------|--------|------|--------|-----------|--------------|------|
| S-001 | Login | E-001 | in_progress | M | 5 | 960 | 225 | [story.md](epics/E-001-user-auth/stories/S-001-login/story.md) |

## Open work sessions

| Item | Actor | Started (UTC) |
|------|-------|---------------|
| T-002 | agent | 2026-07-21T15:00:00Z |

## Items

| ID | Title | Story | Status | Size | Points | Est (min) | Actual (min) | Path |
|----|-------|-------|--------|------|--------|-----------|--------------|------|
| T-001 | Add login API endpoint | S-001 | done | M | 3 | 480 | 225 | [T-001](epics/.../items/T-001-api-endpoint.md) |
```

## Rules

- Paths are relative to the board root
- Include all epics, stories, tasks, and bugs
- Stories under **General** and tasks under **Unattached** appear like any other row (Epic/Story columns show those ids)
- Size column for epics is always `—` (epics have no t-shirt size)
- Epic **Size** is always `—` (epics have no t-shirt size); epic **Points** = sum of story points
- Story **Points** = sum of task/bug points when the story has children
- Open work sessions lists every item with an open Work log row (after idle auto-close, stale sessions should be gone)
- Sort by id ascending within each table
- Prefer one `—` placeholder row when a section is empty
- Also refresh `VELOCITY.md` when syncing
