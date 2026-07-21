# Folder layout

```text
taskmark/
├── README.md
├── INDEX.md
├── SIZING.md
├── VELOCITY.md               # team speed / ETA (from actual_minutes)
├── REPOS.md                  # linked git roots (multi-repo)
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

## Rules

| Artifact | Path pattern |
|----------|----------------|
| Epic | `taskmark/epics/{E-NNN}-{slug}/epic.md` |
| Story | `.../stories/{S-NNN}-{slug}/story.md` |
| Task | `.../items/T-NNN-{slug}.md` |
| Bug | `.../items/B-NNN-{slug}.md` |

- Slug = kebab-case title, ASCII, no trailing slash noise
- One epic file per epic folder (`epic.md`); one story file per story folder (`story.md`)
- Tasks and bugs are sibling files under `items/` (not nested further)
- Scan the board for the next free numeric id before allocating (`E-`, `S-`, `T-`, `B-` namespaces are independent)
