---
name: tkmd-save
description: >-
  Turn a Cursor Plan mode plan into Taskmark epic, story, task, and bug files
  under an existing or new request (2.0 boards), carrying plan diagrams and
  visuals onto the new items.
---

# tkmd-save

Read `taskmark-conventions` first, then apply the same layout detection,
search, request choice, fit, sizing, ID, write-boundary, and
board-writing-language rules as `tkmd-plan`. This command
never implements work. That remains `/tkmd-do` or `/tkmd-save-do`.

## Non-negotiable safety

- Never run `git commit`, `commit-all-repos.sh`, `git push`, or any equivalent.
- Never set an item to `in_progress`.
- Never edit an existing `epic.md`, `story.md`, or leaf, and never edit an
  existing request `brief.md` or meeting file.
- Never generate or refresh `INDEX.md`, `SIZING.md`, `VELOCITY.md`, board
  `README.md`, `CHANGELOG.md`, or `REPOS.md`.
- Creating those new parent files in the same save is allowed; modifying
  pre-existing parent files is not.

## Locate the Cursor plan

Use the first source that yields a complete plan:

1. An explicit plan path, `@` mention, or pasted plan the user supplies.
2. The Plan mode artifact in the current Cursor session (open plan tab or
   conversation plan markdown).
3. Workspace `.cursor/plans/`: newest matching `.md` / `.plan.md` if the user
   just saved the plan to the workspace.
4. Home `~/.cursor/plans/`: Cursor’s default Plan mode location.

If several candidates exist, prefer the one the user named, else the most
recently modified file that matches this session’s topic. If none can be
found, ask for a path rather than inventing scope.

## Search before writing

Search all open and done epics, stories, tasks, and bugs, wherever they live
(`requests/*/epics/**` and legacy `epics/**`). On a request board also search
every request brief (`requests/<slug>/brief.md`) by title, `aliases`, Goal,
Why, and Done when. Compare the plan title, sections, and todos with titles,
descriptions, goals, user stories, acceptance/fix criteria, and parent
context.

If an exact or overlapping item already covers the plan, create nothing.
Report the matching ID and path, then suggest `/tkmd-do` on that match.

Prefer attaching work to an existing fitting story or epic over creating a
parallel hierarchy. Create a new epic only for a distinct initiative that fits
nowhere on the existing board.

## Place the plan in a request

Follow "Choose the request" and "Fit new items into the hierarchy" in
`tkmd-plan`:

- **Request board** (`requests/` exists): when the plan serves an existing
  request, write the new epics, stories, and tasks under
  `requests/<slug>/epics/...` of that request, as new files only, and never
  edit its `brief.md`. When the plan is a new need, create
  `requests/<slug>/brief.md` (id `R-<slug>`, title, `status: proposed` or
  `ready`, `requested_by`, `owner`, `created`; sections Goal, Why, Done when,
  Out of scope, Open questions) plus its epics, stories, and tasks. Fill the
  brief from the plan's context, goal, and success criteria; put unresolved
  plan questions under Open questions.
- **Legacy board** (`epics/` and no `requests/`): keep writing under `epics/`
  and suggest `npx taskmark init`, which migrates the board to requests.

## Map plan sections into Taskmark types

Infer the smallest useful hierarchy from the plan (not from item-type labels
the user must supply):

- initiative/outcome → epic
- user-visible capability → story
- executable unit → task
- defect/regression → bug

Broad plans should become cohesive stories, each split into independently
executable task/bug leaves with clear, observable acceptance or fix criteria.
Do not create parent levels that add no useful grouping.

Use static sizing as a decomposition driver. Split XXL before writing files.
Strongly split XL unless it is one indivisible executable unit. Items created
with children use `size: null` and `points: null`.

Allocate IDs with `scripts/allocate-id.py`. Write only each new item's own
markdown, in the board writing language, using the `tkmd-plan` template. Leave
its log tables empty; the Taskmark App fills them.

## Carry plan diagrams and visuals

Find visuals in the plan: Mermaid fences, markdown images,
HTML `<img>`, ASCII/box diagrams, canvas or `.canvas.tsx` references, attached
image/SVG/PNG files, and other diagram blocks.

Place each visual on the item whose scope it explains:

- Overview architecture or whole-initiative diagrams → the new epic (or the
  new story when no new epic is created). Keep them off an existing brief;
  a new brief may carry the one overview diagram that explains the need.
- Capability-level diagrams → the matching new story.
- Step-level figures, screenshots, and leaf todos → the matching new
  task/bug.

When a visual spans multiple leaves, either duplicate or link it from each
relevant new item, or place it once on the nearest new parent that covers
those leaves. Prefer one parent copy plus relative links from leaves when the
figure is large.

Prefer durable board-friendly forms:

- Keep Mermaid as a fenced `mermaid` block in the item markdown.
- Copy or reference image assets next to the new item when the plan file
  points at a local attachment. Store copies under that item’s directory (for
  example `requests/<slug>/epics/<epic>/stories/<story>/items/assets/`, or
  `epics/<epic>/stories/<story>/items/assets/` on a legacy board) and link with a
  relative markdown image. Do not invent a board-wide media index.
- For canvases, keep a markdown link to the canvas path if it already lives in
  the workspace; otherwise copy the file beside the new item and link it.
- Preserve alt text and captions from the plan when present.

A plan with no visuals still succeeds. Absence of visuals is not an error; do
not add placeholder diagrams.

No new derived board files. Assets live under the board or item paths only as
needed for the new items.

## Report

Return a concise hierarchy with IDs, paths, sizes, parent fit, the request
the work landed in (existing or new), which visuals landed on which items, and
a short rationale. On a legacy board, suggest `npx taskmark init`. If nothing was created, report
the exact or overlapping match. Do not commit.
