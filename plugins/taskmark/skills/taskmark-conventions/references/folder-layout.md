# Folder layout

## Single-project board

Board under the product repo:

```text
my-app/
└── taskmark/
    ├── README.md
    ├── INDEX.md
    ├── SIZING.md
    ├── VELOCITY.md
    ├── REPOS.md
    └── epics/
        └── E-001-user-auth/
            ├── epic.md
            └── stories/
                └── S-001-login/
                    ├── story.md
                    └── items/
                        ├── T-001-api-endpoint.md
                        └── B-001-token-refresh.md
```

## Multi-project board

Dedicated sibling git repo — **repo root is the board** (no nested `taskmark/`):

```text
acme-taskmark/
├── README.md
├── INDEX.md
├── SIZING.md
├── VELOCITY.md
├── REPOS.md
├── epics/
│   └── …
└── .git/
```

## Path patterns

Paths below are relative to the **board root** (`taskmark/` in single mode, or the `*-taskmark` repo root in multi mode).

| Artifact | Path pattern |
|----------|----------------|
| Epic | `epics/{E-NNN}-{slug}/epic.md` |
| Story | `epics/.../stories/{S-NNN}-{slug}/story.md` |
| Task | `.../items/T-NNN-{slug}.md` |
| Bug | `.../items/B-NNN-{slug}.md` |

- Slug = kebab-case title, ASCII, no trailing slash noise
- One epic file per epic folder (`epic.md`); one story file per story folder (`story.md`)
- Tasks and bugs are sibling files under `items/` (not nested further)
- Scan the board for the next free numeric id before allocating (`E-`, `S-`, `T-`, `B-` namespaces are independent)
