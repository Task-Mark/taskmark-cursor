---
name: log-commits
description: >-
  Append git commits to a Taskmark epic, story, task, or bug Commits table,
  including repo short name for multi-repo workspaces. Use after commits land,
  during complete-work, or when the user asks to record commits on a board item.
---

# log-commits

## Prerequisites

- Resolve item id/path.
- Read [commits-log](../taskmark-conventions/references/commits-log.md), [multi-repo](../taskmark-conventions/references/multi-repo.md).
- Ensure the item has a `## Commits` section (add the empty table if missing on older files).

## Steps

1. Determine **since** time: open/closed session Started, `started_at`, or user-provided range.
2. Identify git roots to scan: from `taskmark/REPOS.md`, or discover `.git` directories under the workspace.
3. For each repo, run (from that root):

   ```bash
   git log --since="<ISO or relative>" --pretty=format:'%h|%cI|%s'
   ```

   Filter to commits relevant to this item when possible (paths touched, message keywords, user confirmation).
4. Append new rows `| SHA | Repo | Date (UTC) | Message |` — skip SHAs already listed for that repo on this item.
5. Optionally append the same notable SHAs to parent story and/or epic Commits tables.
6. Bump `updated` on edited files.
7. If multiple linked roots exist, run `sync-taskmark-repos` so every copy gets the commit rows.
8. Reply with the list of commits added.
