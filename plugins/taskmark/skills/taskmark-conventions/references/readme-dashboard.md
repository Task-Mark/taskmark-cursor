# README project dashboard (E-016)

Board-root `README.md` keeps three managed sections (plus Contributors) using HTML markers so scripts never clobber hand-written intro copy.

## Markers

```markdown
<!-- taskmark:project-status:begin -->
## Project status
…
<!-- taskmark:project-status:end -->

<!-- taskmark:open-work:begin -->
## Open work items
…
<!-- taskmark:open-work:end -->

<!-- taskmark:changelog:begin -->
## Changelog
…
<!-- taskmark:changelog:end -->

<!-- taskmark:contributors:begin -->
## Contributors
…
<!-- taskmark:contributors:end -->
```

## Refresh

`scripts/refresh-readme-dashboard.py <board-root>`

Also runs at the end of `recompute-actuals.py` (so `/sync-status` and `/complete-work` update the README).

### Project status

Same headline metrics as the board UI (E-015):

- Total work items (stories + tasks + bugs, excluding cancelled)
- Complete work items (`status: done`)
- Current Speed (90-day weekly points average)

### Open work items

Table of stories, tasks, and bugs that are **not** `done`, `cancelled`, or `blocked: true`.

Columns: ID | Type | Title | Status | Size | Points | Parent

### Changelog

Regenerated from `git log` on the **board repo** (date, short SHA, author, subject). Product-repo commits are out of scope for the initial design.

## Contributors

Still upserted separately via `upsert-readme-contributors.py` when identities are stamped.
