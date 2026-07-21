---
name: sync-plugin-local
description: >-
  Rsync the Taskmark Cursor plugin package into ~/.cursor/plugins/local/taskmark
  after any change to plugins/taskmark in the taskmark-cursor repo. Use after
  editing skills, rules, commands, hooks, scripts, or plugin.json, or when the
  user asks to deploy/sync the local plugin install.
---

# sync-plugin-local

Keep the **installed** local Cursor plugin in sync with this repo. Cursor rejects symlinks outside `~/.cursor/plugins/local`, so every plugin change must be copied.

## When (required)

After **any** edit under `plugins/taskmark/` in the taskmark-cursor project (skills, rules, commands, hooks, scripts, assets, plugin.json, README), run this skill before finishing the turn — do not wait for the user to ask.

Also run when the user says: sync plugin, rsync plugin, deploy local plugin, refresh local install.

## Steps

1. Resolve the plugin package root: directory that contains `.cursor-plugin/plugin.json` and `skills/` (normally `…/taskmark-cursor/plugins/taskmark`).
2. Run the helper (preferred):

   ```bash
   ./scripts/rsync-plugin-local.sh
   ```

   From the plugin package root, or with an explicit source:

   ```bash
   /path/to/taskmark-cursor/plugins/taskmark/scripts/rsync-plugin-local.sh
   ```

   Equivalent manual command:

   ```bash
   mkdir -p ~/.cursor/plugins/local
   rsync -a --delete \
     /absolute/path/to/taskmark-cursor/plugins/taskmark/ \
     ~/.cursor/plugins/local/taskmark/
   ```

3. Confirm `~/.cursor/plugins/local/taskmark/.cursor-plugin/plugin.json` exists and a newly edited file is present under the local copy.
4. Tell the user to **Developer: Reload Window** if skills/commands/rules did not refresh (often needed for new skills).

## Do not

- Symlink the repo into `~/.cursor/plugins/local` (Cursor rejects targets outside that folder).
- Rsync the marketplace repo root — only `plugins/taskmark/`.
- Skip rsync after plugin edits in this repo.
