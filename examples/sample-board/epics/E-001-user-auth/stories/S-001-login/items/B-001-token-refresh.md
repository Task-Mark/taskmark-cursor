---
id: B-001
type: bug
title: Token refresh fails on mobile
status: backlog
priority: high
size: S
size_source: suggested
size_basis: [T-001]
points: 2
points_source: suggested
estimate_minutes: 120
actual_minutes: 0
estimate_basis: [T-001]
session_cap_minutes: 480
parent: S-001
epic: E-001
owner: ""
blocked: false
cancelled: false
tags: [auth, mobile]
created: 2026-07-20
updated: 2026-07-20T16:05:00Z
started_at: null
completed_at: null
---

# B-001: Token refresh fails on mobile

## Description

Mobile clients receive 401 when calling the refresh endpoint after the access token expires.

## Repro steps

1. Log in on iOS
2. Wait for access token expiry
3. Call refresh — observe 401

## Fix criteria

- [ ] Refresh returns new access token on iOS and Android
- [ ] Expired refresh token returns 401 with clear error code
- [ ] Regression test covers refresh flow

## Notes

Likely related to User-Agent or clock skew on device.

## Prompt & feedback log

| # | When (UTC) | Kind | Summary |
|---|------------|------|---------|
| 1 | 2026-07-20T16:00:00Z | prompt | User reported mobile refresh 401 after API login shipped; track as bug under S-001. |

## Commits

| SHA | Repo | Date (UTC) | Message |
|-----|------|------------|---------|

## Work log

| Session | Actor | Started (UTC) | Ended (UTC) | Summary |
|---------|-------|---------------|-------------|---------|
