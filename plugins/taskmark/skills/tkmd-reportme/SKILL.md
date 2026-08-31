---
name: tkmd-reportme
description: >-
  Report the work the current git identity finished since the previous report
  as human-readable bullets in a gitignored .reports/report-YYYYMMDD.md file.
---

# tkmd-reportme

Read `taskmark-conventions` first.

## Non-negotiable safety

- Never run `git commit`, `commit-all-repos.sh`, `git push`, or any equivalent.
- Never edit epic, story, or leaf markdown.
- Never write or refresh `CHANGELOG.md` or the board `README.md`.
- Never generate or refresh `INDEX.md`, `SIZING.md`, `VELOCITY.md`, or
  `REPOS.md`.
- Never run this skill from `/tkmd-do`. Reporting is a separate personal
  command.
- The only write target is `<board>/.reports/report-YYYYMMDD.md`.

## Locate the board

Use the existing canonical board. For one product repository it is
`<repo>/taskmark/`. For multiple repositories it is the dedicated sibling
`<common>-taskmark` root (`epics/` next to `CHANGELOG.md`). If the board is
missing, run the `taskmark-init` skill first, then continue.

Reports live in `<board>/.reports/`. Create that directory when it does not
exist. It is gitignored on purpose: reports are personal and local, never
committed.

Read `taskmark.writingLanguage` from the board `package.json`. If it is
missing, use the language the user usually uses with the Cursor agent (the
init default). Write the title, the period line, category headings, and every
bullet in that language. Chat language does not apply.

## Identify the reporter

Resolve the current git identity with `scripts/git-identity.py`, which returns
name, email, and initials. That identity defines "me" for this report. Report
only leaves this identity resolved; never report someone else's work.

## Resolve the cutoff

1. List `<board>/.reports/` and keep files matching `report-YYYYMMDD.md`.
2. Ignore a file dated today. Today's report is the one being written, so a
   same-day re-run must measure from the previous report and regenerate the
   same file instead of producing an empty one.
3. The cutoff is the newest remaining filename date: include leaves whose
   `completed_at` (fallback `updated`) is strictly after `YYYYMMDD` 23:59:59
   UTC.
4. If no earlier report exists, there is no cutoff: include every qualifying
   leaf, so the first report covers all of that identity's work.

## Collect my done leaves

- Keep `status: done` task and bug leaves under `epics/`.
- Keep only leaves whose `resolvers` contain the current git identity, matching
  on email first and falling back to name or initials.
- Ignore `shelved` and `cancelled` leaves.
- Ignore epics and stories as sources; read them only as parent context for
  wording.

## Wording (Keep a Changelog style, board language)

- One user-visible outcome per bullet, in **past tense**, in the board writing
  language.
- Phrase from the leaf title, user story, or acceptance criteria — not commit
  messages or implementation shorthand.
- **Never** include work-item codes (`T-` / `B-` / `S-` / `E-`, legacy or
  collision-resistant) in visible report text.
- Merging related leaves from the **same story** into one bullet is allowed
  when it reads better.
- Example (English board): `A delete button was added to reference rows.`

Group bullets under Keep a Changelog category headings and omit empty ones.
English equivalents:

```text
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
```

## Write the report

Write `<board>/.reports/report-YYYYMMDD.md` using today's UTC date, overwriting
any file already dated today:

```markdown
# Report 2026-08-31

Work completed by <name> since 2026-08-20.

### Added

- A delete button was added to reference rows.

### Fixed

- The dark-theme background on the board no longer stays light.
```

The period line names the reporter and the cutoff date, or states that this is
the first report and covers everything so far. When nothing qualifies, keep the
title and period line and add a single note that there is nothing new — do not
invent bullets.

## After writing

Report the file path, writing language, cutoff used, how many leaves matched
the identity, and that nothing was committed.
