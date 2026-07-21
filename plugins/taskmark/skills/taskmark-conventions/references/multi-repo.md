# Multi-repo boards

Taskmark supports **single-git** and **multi-git** workspaces. The board lives in **one** place — never as a full copy inside every product repo.

## Modes

### Single-project (one product git root)

- Board lives at `<project>/taskmark/`.
- Board commits use the **project’s** git history.
- `REPOS.md` has one row; Canonical is that project.
- `sync-taskmark-repos` only refreshes `REPOS.md` (no sibling project, no copies).

### Multi-project (two or more product git roots)

- Create a **sibling** git project named `<common_project_name>-taskmark` next to the product projects.
- That project’s **root is the board** — `INDEX.md`, `epics/`, `REPOS.md`, etc. live at `<common>-taskmark/` directly.
- **Do not** nest a second `taskmark/` folder inside (`<common>-taskmark/taskmark/` is wrong).
- Initialize with `git init` if missing.
- Product repos are listed in `REPOS.md` for commit attribution — they must **not** keep a `taskmark/` copy.
- If the common name is **ambiguous**, ask the user (or pass `--name` to the sync script) before creating the folder.

## Deriving `<common_project_name>`

Prefer the first confident rule:

1. All product roots share the same parent directory → use the **parent folder basename**.
2. Else a shared hyphen/underscore **prefix** of the product basenames (at least one segment, e.g. `acme` from `acme-api` / `acme-web`).
3. Else **ambiguous** — do not invent a name; ask the user.

Dedicated board project: `<common_project_name>-taskmark` (hyphen before `taskmark`).

Exclude existing `*-taskmark` board repos from the product-root count when classifying mode.

## Layout comparison

```text
# Single-project
my-app/
└── taskmark/
    ├── INDEX.md
    └── epics/…

# Multi-project (flat board repo)
acme-api/
acme-web/
acme-taskmark/          ← board root == git root
├── INDEX.md
├── REPOS.md
├── epics/…
└── .git/
```

## `REPOS.md`

```markdown
# Linked repositories

Canonical: acme-taskmark

| Name | Path | Git | Last synced (UTC) |
|------|------|-----|-------------------|
| acme-taskmark | /Users/me/work/acme-taskmark | yes | 2026-07-21T15:00:00Z |
| acme-api | /Users/me/work/acme-api | yes | 2026-07-21T15:00:00Z |
| acme-web | /Users/me/work/acme-web | yes | 2026-07-21T15:00:00Z |
```

- **Canonical** = the board git root (`*-taskmark` in multi mode, or the sole product in single mode)
- In multi mode, board files are at Canonical’s **root**, not under a nested `taskmark/`

## Sync rules

1. Run `sync-taskmark-repos` at session start for multi-root work and after board layout changes.
2. Edit the board only under the canonical path — never rsync into product repos.
3. `--migrate`: promote the richest existing board into the dedicated project (flat), then remove leftover `taskmark/` trees from product repos. Also flattens legacy `<name>-taskmark/taskmark/` nests.
4. Single-repo: ensure `REPOS.md` under `<project>/taskmark/`; no sibling `-taskmark` project.

## Agent obligations

- Locate the board via Canonical in `REPOS.md`: multi → Canonical root; single → `<project>/taskmark/`.
- Record commits with the correct **Repo** name from `REPOS.md`.
- On ambiguous naming, **ask the user** before creating `<name>-taskmark`.
