---
name: taskmark-init
description: >-
  Set up or repair a Taskmark board by running the interactive
  `npx taskmark init` CLI and letting the user answer its prompts. Hand-creates
  the 2.0 request board scaffold only when npm/npx is unavailable.
---

# taskmark-init

Read `taskmark-conventions` first.

The Taskmark CLI sets up the board. The agent runs it; the user answers its
prompts. Do not hand-create board files when the CLI can run.

## 1. Run `npx taskmark init`

From the workspace root (the product repository, or the folder that holds the
sibling repositories), run:

```bash
npx taskmark init
```

`npx taskmark` resolves to the CLI of a locally installed `@taskmark/ui`. In a
folder without that install, run `npx @taskmark/ui init` instead: it is the
same CLI and avoids npm fetching an unrelated `taskmark` package.

The command is interactive. Run it in the user's terminal (not in a hidden
background job) and let the user answer each prompt there. Do not guess or
pipe answers on their behalf, and do not pass secrets on the command line.
It asks for, among other things:

- **Board location**: `<product>/taskmark/` for one product repository, or a
  dedicated sibling `<common>-taskmark` repository for several.
- **Git provider**: GitHub or Bitbucket, to connect the Taskmark App that
  reconciles the board on every push and merged pull request.
- **AI key**: an OpenAI or Claude key the App uses for reconciliation. The
  user types it at the CLI's hidden prompt; never ask them to paste it in chat.
- **Agent instructions**: whether to add the Taskmark board instruction to
  `AGENTS.md` and/or `CLAUDE.md`, so any agent works from the board.
- **Board writing language**: any language. If the user has no preference,
  suggest the language they usually use with the Cursor agent. An existing
  `taskmark.writingLanguage` is kept unless they explicitly change it.

On an existing project it also migrates a legacy `epics/` board to requests
(`requests/<slug>/brief.md` plus `requests/<slug>/epics/...`) and runs an
initial reconciliation so the board reflects the work already in git. Let the
user review what it reports.

When the command finishes, summarize what it set up (board path, provider,
whether the App is connected, agent instruction files, migration result) and
anything it asked the user to do next, such as installing the App in the
browser.

Re-running `npx taskmark init` is the repair path: it keeps what is already
configured and fills what is missing.

## 2. Fallback when npm or npx is unavailable

Only when `npx` cannot run at all (no Node.js / npm, or no network), create the
2.0 request board scaffold by hand:

1. Discover product git roots.
   - One root: board = `<product>/taskmark/`.
   - Multiple roots: board = sibling `<common>-taskmark` repository root. Ask
     for the common name when it cannot be derived safely.
2. Create the board directory with `requests/` and `meetings/` (an empty
   `.gitkeep` in each is allowed). Do not create `epics/` on a new board, and
   never move or rewrite an existing `epics/` folder: migration belongs to the
   CLI.
3. Choose the board writing language. Ask the user; any language is allowed.
   Default if they do not pick one: the language they usually use with the
   Cursor agent. If `package.json` already has `taskmark.writingLanguage`, keep
   it unless they explicitly name a different language.
4. Run:

   ```bash
   python3 <plugin>/scripts/ensure-board-ui.py <board-root> --name <board-package-name> --writing-language "<language>"
   ```

   This creates or merges `package.json` (with the `@taskmark/ui` dependency,
   the board scripts, and the `taskmark` block holding `writingLanguage`),
   `vercel.json`, optional `server.js`, Docker stubs, and `.gitignore`. Add
   `--replace-writing-language` only when the user explicitly changes a
   language that is already stored. Omitting `--writing-language` on a repair
   leaves an existing `taskmark.writingLanguage` untouched. Other
   `package.json` keys must not be clobbered. The ignore file must include:

   ```gitignore
   REPOS.md
   .reports/
   node_modules/
   out/
   .taskmark-ui-build/
   .taskmark-ui-dev/
   ```

5. Run `scripts/sync-taskmark-repos.sh` to generate the local-only
   `REPOS.md`. It contains local paths and no `Last synced` field.
6. Tell the user to run `npx taskmark init` later, once npm is available, to
   install `@taskmark/ui`, connect the Taskmark App (GitHub or Bitbucket), set
   the AI key, and add the agent instructions.

Skip `npm install` and `npm run build` in the fallback; they need npm.

## Static project README

The CLI owns the board files. If the user also wants the static project README
and none exists yet, write it from `examples/static-project-readme.md`, in the
board writing language:

- Single-git: product-root `README.md` (not nested `taskmark/README.md`).
- Multi-git: `README.md` at the dedicated sibling `*-taskmark` board root.

Do **not** overwrite a richer hand-written README. Create or replace only when
the file is missing, thinner than this template, or still a generated
dashboard (Last synced, Current speed, open-work list, README changelog).

Never create `INDEX.md`, `SIZING.md`, `VELOCITY.md`, a generated board
dashboard README, or `CHANGELOG.md`. Do not seed a General epic or a
Maintenance request. Never create request briefs, meetings, or items during
init.
