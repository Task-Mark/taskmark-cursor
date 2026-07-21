# INDEX format

Path: `taskmark/INDEX.md`

Maintain this file on every create, status sync, or meaningful board change.

```markdown
# Board index

Last synced: YYYY-MM-DDTHH:MM:SSZ

## Epics

| ID | Title | Status | Size | Path |
|----|-------|--------|------|------|
| E-001 | User authentication | in_progress | M | [epic.md](epics/E-001-user-auth/epic.md) |

## Stories

| ID | Title | Epic | Status | Size | Path |
|----|-------|------|--------|------|------|
| S-001 | Login | E-001 | in_progress | M | [story.md](epics/E-001-user-auth/stories/S-001-login/story.md) |

## Open work sessions

| Item | Actor | Started (UTC) |
|------|-------|---------------|
| T-002 | agent | 2026-07-21T15:00:00Z |

## Items

| ID | Title | Story | Status | Size | Path |
|----|-------|-------|--------|------|------|
| T-001 | Add login API endpoint | S-001 | done | M | [T-001](epics/.../items/T-001-api-endpoint.md) |
```

## Rules

- Paths are relative to `taskmark/`
- Include all epics, stories, tasks, and bugs
- Open work sessions lists every item with an open Work log row
- Sort by id ascending within each table
- If a section has no rows, keep the header and a single placeholder row of `—` cells, or leave the table header with no data rows — prefer one `—` row for clarity
