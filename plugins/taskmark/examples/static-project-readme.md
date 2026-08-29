# Taskmark

Taskmark is conflict-resistant markdown product memory plus a local board UI.
Work lives as epic, story, task, and bug files. Parent status, points, people,
dates, and logs are derived in the UI from descendant leaves — not generated
dashboard markdown.

This file is static project documentation written by `/tkmd-init`. It is not
a generated dashboard: there is no Last synced metric, Current speed, or
open-work list. Release notes live in the board `CHANGELOG.md`, written only
by `/tkmd-changelog` and `/tkmd-version`.

## Product repositories

<!-- Init: list discovered git products by repository name and role. Do not
     paste gitignored local absolute paths from REPOS.md. -->

| Repository | Role |
|------------|------|
| example-taskmark | Board (`epics/` and UI stubs) |
| example-cursor | Cursor plugin |
| example-frontend | Board UI (`@taskmark/ui`) |
| example-website | Public website and docs |

Single-git workspaces have one product repository; the board lives in
`taskmark/` inside that repo.

## Run the board locally

From the **board root** (single-git: `taskmark/` or the product root that
contains it; multi-git: the `*-taskmark` sibling repo):

```bash
npm install
npx taskmark serve
```

The UI listens on [http://localhost:8275](http://localhost:8275).

Live reload while editing board markdown:

```bash
npx taskmark dev
```

`npx taskmark` (the `taskmark` **bin**) works only after a local `@taskmark/ui`
install. Do not run `npx taskmark` in a folder that has not installed that
package — npm may fetch an unrelated `taskmark` package.

## Production build

```bash
npm run build
```

Static HTML and assets are written to `out/`. Preview that export locally:

```bash
npm run preview
```

## Vercel

The board `vercel.json` uses a static `out/` flow (`framework` unset,
`buildCommand`: `npm run build`, `outputDirectory`: `out`). Import the board
repository (or the product repo that contains `taskmark/`) in Vercel and
deploy. `@taskmark/ui` must be a production `dependencies` entry so the install
includes the CLI that emits `out/`.

## Docker

Stubs on the board (`Dockerfile` and `compose.yaml`) build the static export
and serve it on port **8275**:

```bash
docker compose up --build
```

Then open [http://localhost:8275](http://localhost:8275).

## Standalone `@taskmark/ui`

When there is **no** local `@taskmark/ui` install, use the published package
name:

```bash
npx @taskmark/ui
```

That starts **workspace** mode: setup wizard and project picker. Inside a
board folder after `npm install`, `npx taskmark serve` (or `npx taskmark`)
binds that one board. `npx taskmark open` (or `--workspace`) forces the picker
even when a board is nearby.
