# Prompt & feedback log

Required on **stories, tasks, and bugs** (not epics).

```markdown
## Prompt & feedback log

| # | When (UTC) | Kind | Author | Summary |
|---|------------|------|--------|---------|
| 1 | 2026-07-21T13:55:00Z | prompt | Ada Lovelace | User asked for login API with JWT, no session cookies. |
| 2 | 2026-07-21T14:40:00Z | feedback | Ada Lovelace | User rejected cookie fallback; keep JWT-only. |
```

## Rules

1. Kind is only `prompt` or `feedback`.
2. **Author** = current git `user.name` (from `scripts/git-identity.py`) when available; otherwise `agent` or leave blank.
3. Store **faithful summaries** (1–3 sentences). Short prompts may include a brief quoted phrase. Do **not** paste full chat transcripts.
4. Append only — do not rewrite past rows.
5. Do not invent prompts; only log what the user actually said.
6. When the user starts or continues work on an item → append `prompt` before implementing.
7. When the user corrects, accepts, rejects, or reviews → append `feedback`.
8. If one message both gives feedback and new direction, prefer two rows.
9. Row `#` is sequential starting at 1.
