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
points: 3           # 1 | 2 | 3 | 5 | 8 | 13
points_source: suggested # suggested | manual
estimate_minutes: 480    # planned effort
actual_minutes: 0        # sum of billable session minutes; sync updates
estimate_basis: [T-014]  # prior items for estimate / points suggestion
session_cap_minutes: 480 # max billable minutes per session (default 480)
parent: S-001
epic: E-001
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
| `size` / `points` | T-shirt and Fibonacci points together; default map XS→1 … XL→8 |
| `estimate_minutes` | Planned effort; suggested on create |
| `actual_minutes` | Sum of **billable** work-log session minutes only — never `completed_at − started_at` |
| `session_cap_minutes` | Cap per session (default 480). See [effort-time](effort-time.md) |
| `started_at` | Set once on first work-session start (ISO-8601 UTC) |
| `completed_at` | Set when status becomes `done` |
| `updated` | Bump on every meaningful edit |

Epic: `parent: null`, `epic: null`.  
Story: `parent` = epic id, `epic` = same epic id.  
Task/bug: `parent` = story id, `epic` = ancestor epic id.
