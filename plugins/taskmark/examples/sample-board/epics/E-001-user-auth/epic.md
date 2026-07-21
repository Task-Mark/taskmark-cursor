---
id: E-001
type: epic
title: User authentication
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
parent: null
epic: null
owner: ""
blocked: false
cancelled: false
tags: [auth]
created: 2026-07-18
updated: 2026-07-21T12:00:00Z
started_at: 2026-07-19T10:00:00Z
completed_at: null
---

# E-001: User authentication

## Goal

Ship secure login so users can access protected product features.

## Scope

- Email/password login API
- JWT access tokens
- Mobile token refresh fixes

## Out of scope

- Social OAuth providers
- Passwordless / magic links

## Success metrics

- Users can log in and call authenticated APIs
- Token refresh works on iOS and Android

## Stories

- [S-001 Login](stories/S-001-login/story.md) — in_progress

## Commits

| SHA | Repo | Date (UTC) | Message |
|-----|------|------------|---------|
| a1b2c3d | api | 2026-07-19T14:45:00Z | feat(auth): add login endpoint |

## Work log

| Session | Actor | Started (UTC) | Ended (UTC) | Summary |
|---------|-------|---------------|-------------|---------|
| 1 | agent | 2026-07-19T10:00:00Z | 2026-07-19T11:30:00Z | Scaffolded epic and first story |
