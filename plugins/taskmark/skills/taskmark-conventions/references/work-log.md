# Work log

Required on **every** epic, story, task, and bug.

```markdown
## Work log

| Session | Actor | Started (UTC) | Ended (UTC) | Summary |
|---------|-------|---------------|-------------|---------|
| 1 | agent | 2026-07-21T14:00:00Z | 2026-07-21T14:45:00Z | Implemented route + tests |
| 2 | user | 2026-07-21T15:10:00Z | — | In progress: reviewing PR |
```

## Rules

- Open session = `Ended` is `—` or empty
- Actor: `agent`, `user`, or `user:<name>`
- Session numbers are sequential integers starting at 1
- `Summary` = what was done in the session (not the user prompt — that belongs in Prompt & feedback)
- `start-work` opens a session; `complete-work` closes the open session
- Only one open session per item at a time
- On first open session, set frontmatter `started_at` if null
- Always bump `updated` when changing the work log
- **Actual:** billable minutes from these sessions feed `actual_minutes` — see [effort-time](effort-time.md) (idle auto-cap + session cap). Never use calendar span for Actual.
- **Done items must have a work log:** never leave `status: done` with an empty Work log table. Billable total must be **> 2** minutes for delivered work. If historical delivery had no log, backfill one closed session using **points × current 30-day median min/point** (from `VELOCITY.md`), never a ≤2 minute stub. Summary may note `auto-backfilled: velocity × points (missing work log)`.
- Done **stories/epics** should also have sessions (often rollup from children); do not rely only on child logs without a parent Work log row when the parent is `done`.
