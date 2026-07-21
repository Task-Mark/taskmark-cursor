---
id: T-001
type: task
title: Add login API endpoint
status: done
priority: high
size: M
size_source: suggested
size_basis: []
points: 3
points_source: suggested
estimate_minutes: 480
effort_minutes: 285
actual_minutes: 285
estimate_basis: []
session_cap_minutes: 480
parent: S-001
epic: E-001
owner: ""
blocked: false
cancelled: false
tags: [auth, api]
created: 2026-07-18
updated: 2026-07-20T15:00:00Z
started_at: 2026-07-19T11:00:00Z
completed_at: 2026-07-20T15:00:00Z
---

# T-001: Add login API endpoint

## Description

Implement POST /login that validates credentials and returns a JWT access token.

## Acceptance criteria

- [x] Valid credentials return 200 with access token
- [x] Invalid credentials return 401
- [x] Unit tests cover happy path and failure

## Notes

Uses existing auth middleware patterns in the API package.

## Prompt & feedback log

| # | When (UTC) | Kind | Summary |
|---|------------|------|---------|
| 1 | 2026-07-19T10:55:00Z | prompt | User: implement login API with JWT only — no cookie fallback. |
| 2 | 2026-07-20T14:40:00Z | feedback | User approved PR; mark task done after tests pass. |

## Commits

| SHA | Repo | Date (UTC) | Message |
|-----|------|------------|---------|
| a1b2c3d | api | 2026-07-19T14:45:00Z | feat(auth): add login endpoint |
| b2c3d4e | api | 2026-07-20T14:50:00Z | test(auth): cover login failure paths |

## Work log

| Session | Actor | Started (UTC) | Ended (UTC) | Summary |
|---------|-------|---------------|-------------|---------|
| 1 | agent | 2026-07-19T11:00:00Z | 2026-07-19T14:45:00Z | Implemented route + tests |
| 2 | user | 2026-07-20T14:00:00Z | 2026-07-20T15:00:00Z | Reviewed and merged |
