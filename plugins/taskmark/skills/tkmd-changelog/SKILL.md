---
name: tkmd-changelog
description: >-
  Rebuild the Unreleased section of the board CHANGELOG.md from recent done
  task/bug leaves in the board writing language, without work-item IDs.
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

## Collect done leaves

1. Parse existing `CHANGELOG.md` for the newest released heading matching
   `## x.y.z - YYYY-MM-DD` (SemVer, newest section is first after Unreleased).
2. The cutoff is that heading’s date: include leaves whose `completed_at`
   (fallback `updated`) is strictly after `YYYY-MM-DD` 23:59:59 UTC. If there
   is no released heading, include every done task/bug leaf.
3. Ignore `shelved` and `cancelled` leaves. Ignore epics and stories as sources;
   read them only as parent context for wording.
4. Prefer `status: done` task and bug files under `epics/`.

## Wording (Keep a Changelog in the board language)

Rebuild the Unreleased section idempotently from the collected leaves. Preserve
every already-released `## x.y.z - YYYY-MM-DD` section unchanged (do not
retranslate those sections here).

- One user-visible outcome per bullet, in **past tense**, in the board
  writing language.
- Phrase from the user story, acceptance criteria, or title — not commit
  messages or implementation shorthand.
- **Never** include work-item codes (`T-` / `B-` / `S-` / `E-`, legacy or
  collision-resistant) in visible changelog text.
- Merging related leaves from the **same story** into one bullet is allowed
  when it reads better.
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
considered, and that nothing was committed.
