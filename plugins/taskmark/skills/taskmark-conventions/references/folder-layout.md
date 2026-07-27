# Folder layout

## Single-project board

Board under the product repo:

```text
my-app/
└── taskmark/
    ├── README.md
    ├── INDEX.md
    ├── SIZING.md
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
| Task (under story) | `epics/.../stories/.../items/T-NNN-{slug}.md` |
| Bug (under story) | `epics/.../stories/.../items/B-NNN-{slug}.md` |
| Task (under epic) | `epics/{E-NNN}-{slug}/items/T-NNN-{slug}.md` |
| Bug (under epic) | `epics/{E-NNN}-{slug}/items/B-NNN-{slug}.md` |

- Slug = kebab-case title, ASCII, no trailing slash noise
- One epic file per epic folder (`epic.md`); one story file per story folder (`story.md`)
- Tasks and bugs are sibling files under an `items/` folder (story-level or epic-level — not nested further)
- Scan the board for the next free numeric id before allocating (`E-`, `S-`, `T-`, `B-` namespaces are independent)

## Epic-direct tasks and bugs

Tasks and bugs may live **directly under an epic** (no story):

```text
epics/
└── E-001-user-auth/
    ├── epic.md
    ├── items/                 # optional epic-direct leaves
    │   └── T-010-spike.md
    └── stories/
        └── S-001-login/
            ├── story.md
            └── items/
                └── T-001-api.md
```

- Frontmatter: `parent: E-001`, `epic: E-001`
- Prefer a story when the user names one or context is clear; otherwise attach under the epic’s `items/`
- Truly unscoped work (no epic either) still uses the reserved **General** epic’s `items/` and `stories/`

## Reserved General epic

Every board should include a default **General** epic for general tasks and user stories:

```text
epics/
└── E-NNN-general/
    ├── epic.md                 # title: General, tags: [general]
    ├── items/                  # general tasks/bugs (no story)
    └── stories/
        └── …                   # general user stories (optional)
```

- Identify General by title `General`, slug `*-general`, or tag `general` (do not duplicate).
- Run `scripts/ensure-general-epic.py <board-root>` from init and create soft-fallback paths.
- Prefer a contextual epic/story when the user’s prompt clearly matches one; otherwise attach under General.
- Do not delete General; it keeps general tasks and user stories visible in the epic list.
- Never create a catch-all “Unattached” story — story-less tasks/bugs live in epic `items/` only.
