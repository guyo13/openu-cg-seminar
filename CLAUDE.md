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

**`cg-notebook.py` is a thin orchestrator, not the figure code.** It is a marimo
notebook in pure-Python cell format: `@app.cell`-decorated functions whose *parameters*
are their dependencies and whose *return tuple* is what they export to later cells.
marimo regenerates this structure, so edit it through `marimo edit` rather than
hand-rewriting cells — reordering or renaming by hand silently breaks the dataflow
graph, and defining the same name in two cells is a hard error. The `__generated_with`
version string at the top must match the installed marimo.

Every figure function lives in one of three plain modules at the repo root; the notebook
only imports them, calls them, saves the result, and displays it:

| Module | Imported as | Provides |
| --- | --- | --- |
| `chapter2_figures.py` | `lens_geometry`, `slab_geom` | Two no-arg functions returning a Figure |
| `lemma21_sliding_animation.py` | `l2anim` | `animate_case(...)` — writes a GIF, returns its path |
| `scene_figures.py` | `sf` | The D_2 scene plus all Chapter 3 figures |

Prefer adding a figure to the relevant module and calling it from a thin cell. Keeping
plotting code in the notebook is what the modules were extracted to undo.

**Figures are written as a side effect of running the notebook**, to hardcoded relative
paths (`figs/chapter<N>/<topic>/<name>.png`), so always run from the repo root. The
`chapter<N>` numbering tracks *the paper's* sections, not the notebook's own order.
Note `figs/chapter2/perliminaries/` is misspelled and one savefig call contains a double
slash — both work, so leave them alone unless you update every reference together.

**`scene_figures.py` owns the shared visual language.** `TYPE_FACE` / `TYPE_EDGE` map
radius type 1→blue, 2→orange. `make_scene()` builds the 8-disk `BASE_DISKS` arrangement
and computes adjacency plus the *exact* maximum clique by brute force, so
`fig_max_clique` shows a computed result rather than a hand-picked one.
`make_algo_scene()` runs one honest iteration of the algorithm over the extended 11-disk
`ALGO_DISKS` (same disks plus s6/b4/b5), yielding Psi, the slabs, and the X/Y survivors
used by the walk-through figures. Notation figures take `scene`; algorithm figures take
`ascene`.

Every `fig_*` returns a matplotlib Figure and accepts `save=`, which routes through
`_finish` (`dpi=300, bbox_inches="tight"`). The Chapter 3 *notation* cell deliberately
does not use `save=` — it calls `savefig(..., dpi=300)` with no tight crop, matching how
those PNGs were originally produced. The *algorithm* cell does use `save=`. Don't
"unify" these without regenerating and re-committing the affected figures.

**`animate_case(p, q, a, b, case, fname)`** writes a GIF and returns `fname`, so cells
feed it straight into `mo.image`. `case` selects the geometry: `"b"` (exit point slides
along segment ab), `"c"` (slides down a vertical slab wall), `"v"` (degenerate — a and b
share an x-coordinate and the slab collapses to a line). Cases b/c are Figure 1(b)-(c)
of the paper; `"v"` is an added degenerate scenario. In b and c the original ray
p->q->o stays on screen faded and dashed as the baseline, the start point is labelled
`o` and the moving one `o'`; in the degenerate case the two coincide with q, so only the
dashed pq baseline is drawn.

**Inspecting a live notebook.** `marimo[mcp]` is a dependency, so while
`uv run marimo edit cg-notebook.py` is running, the marimo MCP tools can read the live
session: `lint_notebook` and `get_notebook_errors` for validation,
`get_cell_dependency_graph` for variable ownership and multiply-defined names, and
`get_cell_outputs` for rendered results. They are read-only — cell edits still go
through the marimo UI. The server is bound at Claude Code startup, so it is unavailable
in a session that began before it was configured.

## Slides

`slides/` is a self-contained npm project (Slidev v52, seriph theme) — separate from the
uv/Python project at the root.

```bash
cd slides
npm run dev          # live preview
npm run build        # static site -> slides/dist
npm run export:pptx  # -> slides-export.pptx (needs playwright-chromium, already a devDep)
```

### Figures in the deck

Figures are **not** duplicated into `slides/`. They stay at the repo root under `figs/`
and slides reference them relatively (`../figs/chapter2/...`), so regenerating a figure
in the notebook updates the deck with no copy step. That path is outside Slidev's Vite
root, which costs two pieces of config in `slides/vite.config.ts` — both load-bearing:

1. `server.fs.allow` is widened to the repo root. Without it the **build** fails with
   "resolves outside of Vite server.fs.allow".
2. A dev-only plugin (`apply: 'serve'`) serves `/figs/**` from the repo-root `figs/`
   directory. Without it the **build succeeds but `npm run dev` shows broken images** —
   dev leaves the URL literal and base-prefixes it to `/../figs/...`, the browser
   normalises that to `/figs/...`, and Vite's SPA fallback answers with `index.html`.
   The give-away is a 200 with `Content-Type: text/html` where a PNG was expected, so
   check the content type, not the status code.

Dev and build resolve these paths differently, so a passing `npm run build` does not
prove the dev server renders images. Check both.

Do not "fix" any of this by moving figures into `slides/public/`: a `public/figs`
symlink was tried and fails, because Vite's public-dir handling does not follow
directory symlinks.

### LaTeX inside HTML blocks

Math in a raw HTML block only renders if blank lines separate the content from the
tags — CommonMark ends an HTML block at a blank line, and only then is the inner
content markdown-processed (and so KaTeX-processed).

```markdown
<!-- broken: renders the literal text "$\mathcal{C}_1$" -->
<div class="text-sm">
$\mathcal{C}_1$
</div>

<!-- renders: blank line after the opening tag and before the closing one -->
<div class="text-sm">

$\mathcal{C}_1$

</div>
```

The tight form compiles to a raw text node with the `$...$` intact; the spaced form
compiles to KaTeX spans. To audit, build and grep the slides chunk in `slides/dist/`
for surviving `$\...$` literals — any hit is unrendered math.

## Notes and docs

The repo doubles as an Obsidian vault (`.obsidian/` is tracked, and
`.obsidian/workspace.json` churns on every session — this is intentional, leave it
tracked). `docs/` holds the paper PDF, the seminar guidelines PDF, a phased study
checklist, and the running notes, which use Obsidian wikilinks.

`docs/chat-exports/` is gitignored: transcripts pulled from claude.ai chats via
`tools/fetch-claude-chat.js`, which runs against the logged-in browser session (there is
no public API for chat history).
