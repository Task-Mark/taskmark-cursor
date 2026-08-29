---
description: Initialize Taskmark board storage and UI
---

Use the `taskmark-init` skill to initialize or repair the Taskmark board.

Ask for a writing language (any language). If the user does not pick one, use
the language they usually use with the Cursor agent. Persist it on the board
and keep a stored value on repair unless they explicitly change it.

Do not create `INDEX.md`, `SIZING.md`, `VELOCITY.md`, a board `README.md`, or
`CHANGELOG.md`.
