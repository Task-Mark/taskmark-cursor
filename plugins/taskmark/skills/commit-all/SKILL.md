---
name: commit-all
description: >-
  Commit changes in every linked git project in the workspace using a very simple
  one-line commit message per repo (or one shared message). Use when the user
  asks to commit all projects, commit every repo, or run a multi-repo commit action.
---

# commit-all

Commit **every** git project that has changes (from `taskmark/REPOS.md` or discovered `.git` roots).

## Message style (required)

Use a **very simple one-liner** only — no body, no bullet lists, no Conventional Commit scopes unless the user insists.

Good:
- `update login api`
- `fix mobile token refresh`
- `sync taskmark board`
- `add rate limit on login`

Bad:
- multi-paragraph messages
- `feat(auth): implement JWT login with refresh and tests` (too heavy by default)

Prefer lowercase, imperative or noun phrase, under ~72 characters.

## Steps

1. Resolve git roots: `taskmark/REPOS.md` if present, else discover under workspace folders.
2. Optionally run `sync-taskmark-repos` first if `REPOS.md` or board location may be stale.
3. For each root, run `git status --porcelain`. Skip clean repos (report “skipped — clean”).
4. **Generate message** for that repo:
   - If the user gave one message for all repos, use it everywhere.
   - Else derive a simple one-liner from that repo’s changed paths / active Taskmark item title (e.g. `update T-001 login api` or `update auth login`).
   - If only `taskmark/` changed: `sync taskmark board` or `update taskmark board`.
5. In each dirty repo (do not update git config; do not push unless asked):

   ```bash
   git add -A
   git commit -m "$(cat <<'EOF'
   simple one-liner here
   EOF
   )"
   ```

   Prefer the helper: `scripts/commit-all-repos.sh --message "…" [workspace…]` when committing many roots with one shared message; for per-repo messages, commit each root separately following the same one-liner rule.
6. Never commit secrets (`.env`, credentials). Warn and skip those files if present.
7. After commits succeed, run `log-commits` on the active Taskmark item(s) when known; refresh `REPOS.md` via `sync-taskmark-repos` if needed (board lives only in the canonical project).
8. Before the **board-repo** commit (while staging), run
   `python3 <plugin>/scripts/refresh-readme-dashboard.py <board-root>`
   so the changelog includes prior commits and open-work/metrics match board state; stage `README.md` with the board commit. If a board commit already landed without a README refresh, run the script and commit `update readme dashboard` when README is dirty.
9. Reply with a table: Repo | SHA | Message | or “skipped”.

## Safety

- No `--no-verify` unless the user explicitly asks.
- No push, force, or amend unless the user explicitly asks.
- If a repo fails pre-commit hooks, report the error and continue with other repos (or stop if the user asked for all-or-nothing).
