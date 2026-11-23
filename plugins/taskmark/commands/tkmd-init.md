---
description: Set up or repair a Taskmark board with npx taskmark init
---

Use the `taskmark-init` skill to set up or repair the Taskmark board.

Run `npx taskmark init` (or `npx @taskmark/ui init` when `@taskmark/ui` is not
installed locally) in the user's terminal and let the user answer its prompts
there: board location, GitHub or Bitbucket, OpenAI or Claude key, agent
instructions in `AGENTS.md` / `CLAUDE.md`, and the board writing language (any
language; if they have no preference, the language they usually use with the
Cursor agent; a stored value is kept unless they explicitly change it). On an
existing project it migrates a legacy `epics/` board to requests and runs an
initial reconciliation. Never ask for the AI key in chat.

Do not hand-create board files. Only when npm/npx is unavailable, create the
2.0 scaffold (`requests/`, `meetings/`, `package.json` with `@taskmark/ui` and
the `taskmark` block, `.gitignore`) and tell the user to run
`npx taskmark init` later to connect the App.

A static project README may be written only when none exists or it is still a
generated dashboard; never overwrite a richer hand-written README. Do not
create `INDEX.md`, `SIZING.md`, `VELOCITY.md`, or `CHANGELOG.md`.
