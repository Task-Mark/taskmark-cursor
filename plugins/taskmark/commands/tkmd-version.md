---
description: Cut a SemVer, promote CHANGELOG Unreleased, align linked products
---

Use the `tkmd-version` skill to cut a version on the Taskmark board.

This command never commits, pushes, tags, or publishes. It writes the chosen
SemVer to the board `package.json`, every linked product-root `package.json`,
and the Cursor plugin `plugin.json`. It never writes the board README.
