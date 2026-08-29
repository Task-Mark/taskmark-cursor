---
description: Initialize Taskmark board storage and UI
---

Use the `taskmark-init` skill to initialize or repair the Taskmark board.

Ask for a writing language (any language). If the user does not pick one, use
the language they usually use with the Cursor agent. Persist it on the board
and keep a stored value on repair unless they explicitly change it.

Write or repair a **static** project README (purpose, product repositories,
local run, build, Vercel, Docker, `npx @taskmark/ui`) at the product root
(single-git) or the dedicated `*-taskmark` board root (multi-git). Do not
overwrite a richer hand-written README. Do not write a generated dashboard
(Last synced, Current speed, open-work list, README changelog).

Do not create `INDEX.md`, `SIZING.md`, `VELOCITY.md`, or `CHANGELOG.md`.
