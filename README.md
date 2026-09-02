# The Maximum Clique Problem in a Disk Graph Made Easy

Working material for an undergraduate seminar in computational geometry — the
written summary, the presentation deck, and the figures both are built from, for

> J. M. Keil and D. Mondal. *The Maximum Clique Problem in a Disk Graph Made
> Easy.* SoCG 2025. [arXiv:2404.03751](https://doi.org/10.48550/arXiv.2404.03751)

The paper gives an $O(n^{2k}\,\mathrm{poly}(n))$ algorithm for a maximum clique
in a disk graph with $k$ distinct radii, settling the $k = 2$ case that had been
open since Clark–Colbourn–Johnson solved the unit-disk case in 1990.

Seminar summary by Guy Or, The Open University of Israel.

## Layout

| Path | Contents |
| --- | --- |
| `docs/seminal-work/` | The written summary: LaTeX source, bibliography, compiled PDF |
| `docs/` | The paper, seminar guidelines, a phased study checklist, running notes, Q&A reference notes |
| `slides/` | Slidev deck (self-contained npm project) and the exported PPTX |
| `figs/` | Generated figures and animations, `chapter<N>/` tracking the paper's sections |
| `cg-notebook.py` | marimo notebook; renders every figure |
| `chapter2_figures.py` | Lens and slab geometry |
| `lemma21_sliding_animation.py` | Lemma 2.1 sliding animations (GIF) |
| `scene_figures.py` | Section 3 notation and the algorithm walk-through |
| `epilogue_figures.py` | CCJ's lens recipe and its failure for two radii |
| `make_stils.py` | Final frame of each animation as a still, for print |
| `CLAUDE.md` | Repository conventions, for both human and agent contributors |

Figure code lives in the modules; the notebook imports them, calls them, and
writes the results to `figs/`. Nothing under `figs/` is edited by hand.

## Figures

Requires Python ≥ 3.11 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run marimo edit cg-notebook.py   # edit and re-render
uv run marimo run cg-notebook.py    # read-only view
uv run python make_stils.py         # refresh the print stills
```

Run from the repository root; figure output paths are relative to it.

## Written summary

`docs/seminal-work/` contains `main.tex`, `references.bib`, and the compiled
`Guy_Or_CG_Seminar.pdf`. The preamble sets `\graphicspath{{figs/}}` and includes
figures by their repository-relative names, so a `figs/` tree must sit beside
`main.tex` at compile time; the repository keeps no second copy there, and the
PDF is committed instead.

Animations cannot appear in print, so the Lemma 2.1 figures are included as the
stills produced by `make_stils.py`.

## Slides

```bash
cd slides
npm install
npm run dev          # live preview
npm run build        # static site -> slides/dist
npm run export:pptx  # -> slides-export.pptx
```

The deck reads figures directly from `figs/`, so regenerating a figure in the
notebook updates the slides with no copy step. See `CLAUDE.md` for the Vite
configuration this requires, and for the blank-line rule that makes LaTeX render
inside the deck's HTML blocks.

## Notes

The notes under `docs/` are an Obsidian vault. They use wikilinks and inline
LaTeX, and read best in Obsidian, though they render acceptably on GitHub.
`qa-armor-notes.md` is podium reference material rather than slide content.
