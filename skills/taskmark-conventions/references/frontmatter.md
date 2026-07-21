# Frontmatter

Every work item file starts with YAML frontmatter:

```yaml
---
id: T-001
type: task          # epic | story | task | bug
title: Add login API endpoint
status: backlog     # derived — do not hand-set except via latches
priority: medium    # critical | high | medium | low
size: M             # XS | S | M | L | XL
size_source: suggested   # suggested | manual
size_basis: [T-014, T-022]
parent: S-001       # story→epic; task/bug→story; epic→null
epic: E-001         # denormalized on story/task/bug; null on epic
owner: ""
blocked: false
cancelled: false
tags: []
created: 2026-07-21
updated: 2026-07-21T15:02:00Z
started_at: null
completed_at: null
---
```

## Field notes

| Field | Rules |
|-------|--------|
| `status` | Derived by sync-status. Do not edit directly. |
| `blocked` / `cancelled` | Manual latches that force status |
| `size_basis` | Prior item ids used for suggestion; `[]` if manual or none |
| `started_at` | Set once on first work-session start (ISO-8601 UTC) |
| `completed_at` | Set when status becomes `done` |
| `updated` | Bump on every meaningful edit (ISO-8601 UTC preferred) |
| `created` | Date or datetime when the file was created |

Epic: `parent: null`, `epic: null`.  
Story: `parent` = epic id, `epic` = same epic id.  
Task/bug: `parent` = story id, `epic` = ancestor epic id.
