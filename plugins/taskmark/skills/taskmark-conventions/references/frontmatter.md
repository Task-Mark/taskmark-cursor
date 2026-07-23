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
estimate_minutes: 480    # Est: velocity × points or seed
actual_minutes: 0        # Actual: billable start-work→complete-work sessions
estimate_source: suggested  # suggested | manual
estimate_basis: [T-014]  # prior items or [velocity:30d:Nmin/pt]
session_cap_minutes: 480 # max billable minutes per session (default 480)
parent: S-001
epic: E-001
owner: ""
reporters: []
resolvers: []
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
| `owner` | Optional display string; prefer `reporters` / `resolvers` for attribution |
| `reporters` / `resolvers` | Lists of `{name, email, initials}` from git config — see [identity](identity.md) |
| `size` / `points` | Tasks/bugs use t-shirt + Fibonacci. Stories roll points from tasks. **Epics have no size** (`null`); epic points = sum of story points **plus epic-direct task/bug points**. |
| `estimate_minutes` | **Est** — planned time from 30-day velocity × points or seeds |
| `estimate_source` | `suggested` (may refresh on calibrate) or `manual` (never overwrite) |
| `actual_minutes` | **Actual** — billable work-log sessions from start-work / complete-work |
| `session_cap_minutes` | Cap per session for Actual (default 480). See [effort-time](effort-time.md) |
| `started_at` | Set on start (leaf + parent cascade). ISO-8601 UTC |
| `completed_at` | Set when status becomes `done` (leaf + parent end cascade) |
| `updated` | Bump on every meaningful edit |

Epic: `parent: null`, `epic: null`.  
Story: `parent` = epic id, `epic` = same epic id (preferred). May be `null` only transiently; prefer attaching under the reserved **General** epic when no clearer epic fits.  
Task/bug under a story: `parent` = story id, `epic` = ancestor epic id.  
Task/bug under an epic (no story): `parent` = epic id, `epic` = same epic id. Files live in `epics/{E-NNN}/items/`.

### Optional hierarchy

- Stories and tasks do **not** require a user-invented epic/story. Soft-attach from prompt/context when possible; otherwise use **General**.
- Reserved epic: title `General`, folder slug `{E-NNN}-general`, tag `general`. Do not delete; recreate via `ensure-general-epic.py` if missing.
- Files always live under `epics/…` — either `stories/…/items/` or epic-level `items/`. “Standalone” means optional *user* hierarchy, not free-floating markdown outside that tree.
- Do **not** use a catch-all Unattached story; story-less tasks/bugs attach under an epic’s `items/` (or General’s `items/` when no epic is clear).
