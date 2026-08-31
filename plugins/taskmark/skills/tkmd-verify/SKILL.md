---
name: tkmd-verify
description: >-
  Migrate an existing Taskmark board to the current layout: repair scaffold,
  delete leftover generated files, and strip legacy item markdown.
---

# tkmd-verify

Read `taskmark-conventions` first.

Migrate an **existing** board to today’s layout. Keep `/tkmd-init` as first
create / light repair. Do not skip discovery. Do not translate item bodies or
rewrite IDs.

## Non-negotiable safety

- Never run `git commit`, `commit-all-repos.sh`, `git push`, or any equivalent.
- Never create `INDEX.md`, `SIZING.md`, `VELOCITY.md`, or `CHANGELOG.md`.
- Never delete an existing `CHANGELOG.md`, `epics/`, `node_modules/`, or `out/`.
- Never set an item to `in_progress`.
- Default is apply plus a summary. If the user asks not to write yet, run
  `verify-board.py --dry-run` and report what would change.

## Four phases

### 1. Locate the canonical board

Use the same discovery as `taskmark-init` and `sync-taskmark-repos.sh`:

- One product git root: `<product>/taskmark/`.
- Multiple product git roots: sibling `<common>-taskmark` repository root
  (`epics/` at that root).

If the board is missing, run `taskmark-init` first, then continue. Extra
`taskmark/` trees in product repos are **reported**, not deleted, unless they
are clearly generated duplicates (only leftover INDEX/SIZING/VELOCITY/ID
counters and no real epic markdown).

### 2. Repair the scaffold like init

Keep `taskmark.writingLanguage` when it is already stored. Fill it only when
missing (init default: the language the user usually uses with the Cursor
agent). Do not pass `--replace-writing-language` unless the user explicitly
changes the language.

Run:

```bash
python3 <plugin>/scripts/ensure-board-ui.py <board-root> --name <board-package-name>
```

Omit `--writing-language` on a repair so an existing stored language is kept.
Pass `--writing-language` only to fill a missing field.

Ensure `.gitignore` lists `REPOS.md` and `.reports/`. Install `@taskmark/ui`
as a production dependency (`npm install @taskmark/ui --save`). Run
`scripts/sync-taskmark-repos.sh` so local `REPOS.md` exists.

Write or repair the **static project README** with the same overwrite rules as
init (`examples/static-project-readme.md`, board writing language):

- Single-git: product-root `README.md`, not nested `taskmark/README.md`.
- Multi-git: `README.md` at the dedicated sibling `*-taskmark` board root.
- Create or replace only when the file is missing, thinner than the template,
  or still a generated dashboard (Last synced, Current speed, open-work list,
  README changelog). Do not overwrite a richer hand-written README.

### 3. Delete leftover generated files

At the **canonical board root only**, run:

```bash
python3 <plugin>/scripts/verify-board.py <board-root> [--dry-run] [--workspace <workspace>…]
```

The script removes `INDEX.md`, `SIZING.md`, `VELOCITY.md`, and shared ID
counter files (`NEXT_IDS`, `NEXT_IDS.md`, and similar) when present. After the
static README lives in the init location, it deletes a nested generated
dashboard README (`taskmark/README.md` in single-git, or `taskmark/README.md`
under a multi-git board). It does not create those files.

### 4. Migrate item markdown

The same `verify-board.py` scan of `epics/**/*.md` is mechanical only:

- Strip retired frontmatter: `owner`, `estimate_minutes`, `estimate_source`,
  `estimate_basis`, `actual_minutes`, `actual_ms`, `size_source`, `size_basis`,
  `points_source`, `session_cap_minutes`.
- Keep current spec keys, titles, bodies, acceptance criteria, and
  `in_progress` status. Do not rewrite IDs (legacy sequential IDs stay valid).
- On `epic.md` and `story.md` only, remove child-list sections (`## Stories`
  and similar) and parent Commits / Work log / Prompt & feedback sections.
- Do not strip Prompt & feedback, Commits, or Work log from task/bug leaves.

## Report

Print the JSON from `verify-board.py` (deleted paths, rewritten file count,
extra `taskmark/` copies). Summarize scaffold repairs. Never commit or push.
