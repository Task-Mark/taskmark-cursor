# Contributor identity (git config)

Taskmark attributes work to people using the **local git config** identity
(`user.name` / `user.email`), not browser OAuth. The browser never reads git
config; the Cursor plugin / agent stamps identity when creating or completing
items.

## Identity shape

Each person is stored as:

```yaml
name: Ada Lovelace
email: ada@example.com
initials: AL
```

| Field | Rules |
|-------|--------|
| `name` | From `git config user.name` (fallback: email local-part) |
| `email` | From `git config user.email` (may be empty) |
| `initials` | Derived when missing: first letter of first + last name token; single token → first 1–2 letters; uppercased |

## Work-item fields

On every epic, story, task, and bug frontmatter:

```yaml
reporters: []   # who created / reported the item (multi-author OK)
resolvers: []   # who completed / developed the item (multi-author OK)
```

Example:

```yaml
reporters:
  - name: Ada Lovelace
    email: ada@example.com
    initials: AL
resolvers:
  - name: Alan Turing
    email: alan@example.com
    initials: AT
```

### Rules

1. **reporters** — stamped on `create-epic` / `create-story` / `create-task` from current git identity.
2. **resolvers** — stamped on `complete-work` from current git identity.
3. **Uniqueness** — merge by email (case-insensitive). Same email is not duplicated; fill missing name/initials on merge.
4. Multiple distinct emails accumulate (multi-author / multi-developer).
5. Missing git config → leave lists unchanged / empty; do not block board writes.
6. `owner` may remain for display; **reporters** / **resolvers** are the attribution source of truth for avatars and README contributors.

## UI hover copy

- Created only → `Created by <name>`
- Resolved only → `Resolved by <name>`
- Same person both → one avatar → `Created and developed by <name>`
- Multiple people → multiple avatars with role-appropriate labels

## README contributors

Product / board `README.md` files get a managed block:

```markdown
<!-- taskmark:contributors:begin -->
## Contributors
...
<!-- taskmark:contributors:end -->
```

Upsert via `scripts/upsert-readme-contributors.py` when a new identity is stamped.
Use `scripts/git-identity.py` to read or merge the current git user.

Managed project-status / open-work / changelog sections: see [readme-dashboard](readme-dashboard.md).

## Activity authors

- **Commits** table includes an **Author** column (git commit author).
- **Work log** **Actor** uses the human git `user.name` when available.
- **Prompt & feedback** table includes an **Author** column stamped from git identity.
