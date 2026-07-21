---
id: S-001
type: story
title: Login
status: in_progress
priority: high
size: M
size_source: suggested
size_basis: []
points: 5
points_source: suggested
estimate_minutes: 600
actual_minutes: 285
estimate_basis: []
session_cap_minutes: 480
parent: E-001
epic: E-001
owner: ""
blocked: false
cancelled: false
tags: [auth, login]
created: 2026-07-18
updated: 2026-07-21T12:00:00Z
started_at: 2026-07-19T10:15:00Z
completed_at: null
---

# S-001: Login

## User story

As a registered user, I want to log in with email and password so that I can access my account.

## Acceptance criteria

- [x] POST /login returns JWT for valid credentials
- [ ] Token refresh works on mobile clients
- [ ] Invalid credentials return 401 without leaking whether email exists

## Tasks

- [T-001 Add login API endpoint](items/T-001-api-endpoint.md) — done
- [B-001 Token refresh fails on mobile](items/B-001-token-refresh.md) — backlog

## Prompt & feedback log

| # | When (UTC) | Kind | Summary |
|---|------------|------|---------|
| 1 | 2026-07-19T10:10:00Z | prompt | User asked for email/password login with JWT, no session cookies. |
| 2 | 2026-07-20T16:00:00Z | feedback | User accepted API shape; asked to track mobile refresh as a bug. |

## Commits

| SHA | Repo | Date (UTC) | Message |
|-----|------|------------|---------|
| a1b2c3d | api | 2026-07-19T14:45:00Z | feat(auth): add login endpoint |

## Work log

| Session | Actor | Started (UTC) | Ended (UTC) | Summary |
|---------|-------|---------------|-------------|---------|
| 1 | agent | 2026-07-19T10:15:00Z | 2026-07-19T14:00:00Z | Created story and login API task |
