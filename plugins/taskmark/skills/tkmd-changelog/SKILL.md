---
name: tkmd-changelog
description: >-
  Rebuild the Unreleased section of the board CHANGELOG.md from recent done
  work and post-release follow-ups on done leaves, in the board writing
  language, without work-item IDs.
---

# tkmd-changelog

Read `taskmark-conventions` first.

## Non-negotiable safety

- Never run `git commit`, `commit-all-repos.sh`, `git push`, or any equivalent.
- Never edit epic, story, or leaf markdown.
- Never write or refresh the board `README.md`.
- Never generate or refresh `INDEX.md`, `SIZING.md`, `VELOCITY.md`, or
  `REPOS.md`.
- Never run this skill from `/tkmd-do`. Changelog is a separate maintainer
  command.

## Locate the board

Use the existing canonical board. For one product repository it is
`<repo>/taskmark/CHANGELOG.md`. For multiple repositories it is the dedicated
sibling `<common>-taskmark` root (`CHANGELOG.md` next to `epics/`). If the
board is missing, run the `taskmark-init` skill first, then continue.

Write **only** that board-root `CHANGELOG.md`. Create the file if it does not
exist. Never put changelog sections in a README.

Read `taskmark.writingLanguage` from the board `package.json`. If it is
missing, use the language the user usually uses with the Cursor agent (the
init default). Write intro, Unreleased, category headings, and new bullets in
that language. Chat language does not apply.

## Collect done work

1. Parse existing `CHANGELOG.md` for the newest released heading matching
   `## x.y.z - YYYY-MM-DD` (SemVer, newest section is first after Unreleased).
   The cutoff is that heading’s date at `YYYY-MM-DD` 23:59:59 UTC. If there
   is no released heading, include every done task/bug leaf (treat the whole
   leaf as newly completed).
2. Scan `status: done` task and bug files under `epics/`. Ignore `shelved` and
   `cancelled` leaves. Ignore epics and stories as sources; read them only as
   parent context for wording.
3. A leaf qualifies when **any** of these is strictly after the cutoff:
   - `completed_at` (fallback `updated`)
   - a Prompt & feedback row whose kind is `prompt` or `feedback` and whose
     When (UTC) timestamp is after cutoff
   - a Work log row whose Ended (UTC) is after cutoff
4. Split events on a qualifying leaf:
   - **Initial completion** — only when `completed_at` (fallback `updated`) is
     after cutoff: phrase from title, user story, or acceptance criteria.
   - **Follow-ups after cutoff** — one user-visible outcome per distinct
     Work log summary whose Ended is after cutoff (preferred). If a prompt or
     feedback row has no matching work-log summary, paraphrase that row into
     a past-tense outcome. Do **not** restate the original title or first
     shipped outcome when `completed_at` is on or before cutoff.
5. Drop a bullet when the same outcome already appears in a released
   `## x.y.z - YYYY-MM-DD` section. Skip empty, sync-only, or non-user-facing
   rows.

## Wording (Keep a Changelog in the board language)

Rebuild the Unreleased section idempotently from the collected events.
Preserve every already-released `## x.y.z - YYYY-MM-DD` section unchanged
(do not retranslate those sections here).

- One user-visible outcome per bullet, in **past tense**, in the board
  writing language.
- Phrase from the user story, acceptance criteria, title, **or** post-cutoff
  Work log / Prompt & feedback rows — not commit messages or implementation
  shorthand. Prefer Work log `Summary`, then prompt, then feedback.
- **Never** include work-item codes (`T-` / `B-` / `S-` / `E-`, legacy or
  collision-resistant) in visible changelog text.
- Merging related leaves or follow-ups from the **same story** into one
  bullet is allowed when it reads better.
- Example (English board): `A button to filter completed tasks was added.`

Translate Keep a Changelog headings into the stored language. English
equivalents:

```text
# Changelog
## Unreleased
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
## x.y.z - YYYY-MM-DD
```

Omit empty `###` categories. If nothing qualifies, keep Unreleased with no
category subsections (or a single note that there is nothing new) and do not
invent bullets.

When creating the file, use a short Keep a Changelog intro in the board
language, then Unreleased, then any existing released sections (none on first
create).

## After writing

Report the board path, writing language, cutoff used, how many leaves were
considered (newly completed vs follow-up-only), and that nothing was
committed.
