# The Maximum Clique Problem in a Disk Graph Made Easy

Working material for an undergraduate seminar in computational geometry: study
notes, generated figures, and the presentation deck for

> J. M. Keil and D. Mondal. *The Maximum Clique Problem in a Disk Graph Made
> Easy.* SoCG 2025. [arXiv:2404.03751](https://doi.org/10.48550/arXiv.2404.03751)

The paper gives an $O(n^{2k}\,\mathrm{poly}(n))$ algorithm for a maximum clique
in a disk graph with $k$ distinct radii, settling the $k = 2$ case that had been
open since Clark–Colbourn–Johnson solved the unit-disk case in 1990.

## Layout

| Path | Contents |
| --- | --- |
| `docs/` | The paper, seminar guidelines, a phased study checklist, running notes, and Q&A reference notes |
| `figs/` | Generated figures and animations, `chapter<N>/` tracking the paper's sections |
| `slides/` | Slidev deck (self-contained npm project) |
| `cg-notebook.py` | marimo notebook; renders every figure |
| `chapter2_figures.py` | Lens and slab geometry |
| `lemma21_sliding_animation.py` | Lemma 2.1 sliding animations (GIF) |
| `scene_figures.py` | Section 3 notation and the algorithm walk-through |
| `epilogue_figures.py` | CCJ's lens recipe and its failure for two radii |
| `CLAUDE.md` | Repository conventions, for both human and agent contributors |

Figure code lives in the modules; the notebook imports them, calls them, and
writes the results to `figs/`. Nothing under `figs/` is edited by hand.

## Figures

Requires Python ≥ 3.11 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run marimo edit cg-notebook.py   # edit and re-render
uv run marimo run cg-notebook.py    # read-only view
```

Run from the repository root; figure output paths are relative to it.

## Slides

```bash
cd slides
npm install
npm run dev          # live preview
npm run build        # static site -> slides/dist
npm run export:pptx  # -> slides-export.pptx
```

The deck references figures directly from `figs/`, so regenerating a figure in
the notebook updates the slides with no copy step. See `CLAUDE.md` for the Vite
configuration this requires.

## Notes

The repository doubles as an Obsidian vault, with the notes under `docs/`. They
use wikilinks and inline LaTeX, and read best in Obsidian, though they render
acceptably on GitHub.
