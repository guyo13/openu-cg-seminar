# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Not a software project — it is the working material for an undergraduate computational
geometry seminar talk on Keil & Mondal, *The Maximum Clique Problem in a Disk Graph Made
Easy* (SoCG 2025, arXiv:2404.03751). The code exists only to produce figures and
animations for the notes and slides. There are no tests and no linter; don't add
software-project scaffolding unless asked.

`main.py` is the leftover `uv init` stub and is unused.

## Commands

```bash
uv sync                            # install deps
uv run marimo edit cg-notebook.py  # main workflow: edit + re-render figures
uv run marimo run cg-notebook.py   # read-only app view
uv run python lemma21_sliding_animation.py   # module is import-only; no __main__
```

Always run from the repo root — every figure output path in the notebook is relative.

## Architecture

**`cg-notebook.py` is the single source of every figure.** It is a marimo notebook in
pure-Python cell format: `@app.cell`-decorated functions whose *parameters* are their
dependencies and whose *return tuple* is what they export to later cells. marimo
regenerates this structure, so edit it through `marimo edit` rather than hand-rewriting
cells — reordering or renaming by hand silently breaks the dataflow graph. The
`__generated_with` version string at the top must match the installed marimo.

**Figures are written as a side effect of running the notebook.** Cells call
`fig.savefig("figs/chapter<N>/<topic>/<name>.png", dpi=300)` with hardcoded paths.
The `chapter<N>` numbering tracks *the paper's* sections, not the notebook's own order.
Note the directory `figs/chapter2/perliminaries/` is misspelled and one savefig call
contains a double slash — both work, so leave them alone unless you update every
reference together.

**`lemma21_sliding_animation.py` is the only local module the notebook imports**
(`import lemma21_sliding_animation as l2anim`). Standalone matplotlib + `PillowWriter`.
Its entry point is `animate_case(p, q, a, b, case, fname)`, which writes a GIF and
returns `fname` so notebook cells can feed the result straight into `mo.image`. The
`case` argument selects the geometry: `"b"` (exit point slides along segment ab),
`"c"` (slides down a vertical slab wall), `"v"` (degenerate — a and b share an
x-coordinate and the slab collapses to a line). Cases b/c correspond to Figure 1(b)-(c)
of the paper; `"v"` is an added degenerate scenario.

**Shared visual conventions.** `TYPE_FACE` / `TYPE_EDGE` (defined in the first cell) map
radius type 1→blue, 2→orange and are used by every Chapter 3 figure. `make_scene()`
builds the example D_2 arrangement and computes both adjacency and the *exact* maximum
clique by brute force, so `fig_max_clique` shows a computed result rather than a
hand-picked one. Each `fig_*(scene, save=None)` returns a matplotlib Figure; `_draw` and
`_finish` are the shared internals.

## Slides

`slides/` is a self-contained npm project (Slidev v52, seriph theme) — separate from the
uv/Python project at the root.

```bash
cd slides
npm run dev          # live preview
npm run build        # static site -> slides/dist
npm run export:pptx  # -> slides-export.pptx (needs playwright-chromium, already a devDep)
```

Figures are **not** duplicated into `slides/`. They stay at the repo root under `figs/`
and slides reference them relatively (`../figs/chapter2/...`), which is outside Slidev's
Vite root — hence `slides/vite.config.ts` widens `server.fs.allow` to the repo root.
Do not "fix" this by moving figures into `slides/public/`: a `public/figs` symlink was
tried and fails, because Vite's public-dir handling does not follow directory symlinks.
Regenerating a figure in the notebook updates the deck with no copy step.

## Notes and docs

The repo doubles as an Obsidian vault (`.obsidian/` is tracked, and
`.obsidian/workspace.json` churns on every session — this is intentional, leave it
tracked). `docs/` holds the paper PDF, the seminar guidelines PDF, a phased study
checklist, and the running notes, which use Obsidian wikilinks.

`docs/chat-exports/` is gitignored: transcripts pulled from claude.ai chats via
`tools/fetch-claude-chat.js`, which runs against the logged-in browser session (there is
no public API for chat history).
