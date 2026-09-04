# scene_figures.py — single home for the D_2 example arrangement and every
# figure drawn on it (Chapter 3 notation + Chapter 3 algorithm walk-through).
#
# The marimo notebook should hold only thin cells:
#
#     import scene_figures as sf
#     scene  = sf.make_scene()                    # 8-disk scene (notation figs)
#     ascene = sf.make_algo_scene()               # 11-disk scene + one full run
#     fig = sf.fig_guess(ascene); fig.savefig("figs/chapter3/algorithm/guess.png", dpi=300)
#
# Every fig_* returns a matplotlib Figure and accepts save="path.png".

import itertools
from types import SimpleNamespace

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

TYPE_FACE = {1: "#a5d8ff", 2: "#ffd8a8"}      # fill by radius type
TYPE_EDGE = {1: "#1971c2", 2: "#e8590c"}
PSI_EDGE  = "#2f9e44"                         # guessed anchors (Psi) - green
X_EDGE    = "#7048e8"                         # upper-slab survivors  - violet
Y_EDGE    = "#d6336c"                         # lower-slab survivors  - magenta
EPS       = 1e-12

# per-disk label nudges (points) to keep the crowded core legible
LABEL_OFFSETS = {
    "s1": (-24, 6), "s2": (7, 6), "s3": (-8, 10),
    "s6": (-26, -3), "b2": (6, -14), "b4": (6, 8),
}

R1, R2 = 0.8, 1.4

# the original 8-disk arrangement (notation figures) ...
BASE_DISKS = [  # (x,     y,    radius, name)
    ( 0.0,  0.0, R1, "s1"),
    ( 1.1,  0.2, R1, "s2"),
    ( 0.5,  0.9, R1, "s3"),
    ( 2.6, -0.5, R1, "s4"),
    (-1.6, -1.4, R1, "s5"),
    ( 1.8,  1.2, R2, "b1"),
    ( 0.9, -1.0, R2, "b2"),
    (-2.4,  0.6, R2, "b3"),
]
# ... extended for the algorithm walk-through: s6 joins the lower type-1 slab
# (but misses s3!), b4 joins the upper type-2 slab, b5 sits in a slab yet
# fails the Psi-intersection filter.
ALGO_DISKS = BASE_DISKS + [
    ( 0.75, -0.72, R1, "s6"),
    ( 1.2,   0.6,  R2, "b4"),
    ( 1.7,  -3.0,  R2, "b5"),
]


def make_scene(r1=R1, r2=R2, disks=None):
    """Build an arrangement; compute adjacency and the exact maximum clique
    (brute force on the geometry)."""
    disks = disks if disks is not None else BASE_DISKS
    pos = np.array([[d[0], d[1]] for d in disks])
    rad = np.array([d[2] for d in disks])
    nam = [d[3] for d in disks]
    n = len(disks)
    typ = [1 if r == r1 else 2 for r in rad]

    adj = [[i != j and np.linalg.norm(pos[i] - pos[j]) <= rad[i] + rad[j] + EPS
            for j in range(n)] for i in range(n)]

    def _is_clique(S):
        return all(adj[i][j] for i, j in itertools.combinations(S, 2))

    cmax = max((S for m in range(n, 0, -1)
                for S in itertools.combinations(range(n), m) if _is_clique(S)),
               key=len)
    return SimpleNamespace(
        pos=pos, rad=rad, name=nam, n=n, typ=typ, adj=adj,
        cmax=list(cmax),
        c1=[i for i in cmax if typ[i] == 1],   # calligraphic C_1
        c2=[i for i in cmax if typ[i] == 2],   # calligraphic C_2
    )


# --------------------------------------------------------------------------
# the algorithm's state for ONE guess (default: the provably correct guess)
# --------------------------------------------------------------------------

def make_algo_scene(scene=None, guess=None):
    """Run one iteration of the Section 3 algorithm and record every
    intermediate object, so figures can show the run honestly.

    guess: dict {type: (ai_index, bi_index)}; None derives the correct guess
    (leftmost/rightmost centers per type of the true maximum clique)."""
    s = scene if scene is not None else make_scene(disks=ALGO_DISKS)

    if guess is None:
        guess = {}
        for t in sorted(set(s.typ[i] for i in s.cmax)):
            members = [i for i in s.cmax if s.typ[i] == t]
            guess[t] = (min(members, key=lambda i: s.pos[i][0]),
                        max(members, key=lambda i: s.pos[i][0]))

    psi = sorted({i for ab in guess.values() for i in ab})
    psi_valid = all(s.adj[i][j] for i, j in itertools.combinations(psi, 2))

    def seg_y(t, x):
        ai, bi = guess[t]
        (xa, ya), (xb, yb) = s.pos[ai], s.pos[bi]
        if abs(xb - xa) < EPS:
            return ya  # degenerate; callers also check the x-interval
        return ya + (yb - ya) * (x - xa) / (xb - xa)

    def in_slab(i, upper):
        t = s.typ[i]
        if t not in guess:
            return False
        ai, bi = guess[t]
        x, y = s.pos[i]
        xa, xb = sorted((s.pos[ai][0], s.pos[bi][0]))
        if not (xa - EPS <= x <= xb + EPS):
            return False
        return y >= seg_y(t, x) - EPS if upper else y <= seg_y(t, x) + EPS

    def meets_all_psi(i):
        return all(s.adj[i][j] for j in psi if j != i)

    X, Y, reasons = [], [], {}
    for i in range(s.n):
        if i in psi:
            continue
        if not (in_slab(i, True) or in_slab(i, False)):
            reasons[i] = "slab"           # center outside its type's slab
        elif not meets_all_psi(i):
            reasons[i] = "psi"            # misses some guessed disk
        elif in_slab(i, True):
            X.append(i)
        else:
            Y.append(i)

    cand = X + Y
    # missing adjacencies inside the candidate set = edges of the complement H
    comp_edges = [(i, j) for i, j in itertools.combinations(cand, 2)
                  if not s.adj[i][j]]
    # max clique of the candidate graph (tiny: brute force = the matching step)
    best = max((S for m in range(len(cand), -1, -1)
                for S in itertools.combinations(cand, m)
                if all(s.adj[i][j] for i, j in itertools.combinations(S, 2))),
               key=len)
    final = sorted(set(psi) | set(best))

    # maximum matching in the complement H (brute force; H is tiny) —
    # Koenig: |max matching| = |X ∪ Y| − |max independent set of H|
    matching = max(
        (M for m in range(len(comp_edges), -1, -1)
         for M in itertools.combinations(comp_edges, m)
         if len({v for e in M for v in e}) == 2 * len(M)),
        key=len)

    return SimpleNamespace(
        s=s, guess=guess, psi=psi, psi_valid=psi_valid,
        X=X, Y=Y, reasons=reasons, comp_edges=comp_edges,
        matching=list(matching),
        chosen=list(best), final=final, seg_y=seg_y,
    )


# --------------------------------------------------------------------------
# shared drawing helpers
# --------------------------------------------------------------------------

def _limits(s, pad=0.4):
    lo = (s.pos - s.rad[:, None]).min(axis=0) - pad
    hi = (s.pos + s.rad[:, None]).max(axis=0) + pad
    return (lo[0], hi[0]), (lo[1], hi[1])

def _base_axes(s, figsize=(8.2, 6.0)):
    fig, ax = plt.subplots(figsize=figsize)
    xlim, ylim = _limits(s)
    ax.set_aspect("equal"); ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax

def _disk(ax, s, i, edge, lw=1.2, alpha=.85, label_alpha=1.0, fill=True,
          accent=False, ls="-"):
    """accent=True: the center point and the name label take the edge color,
    tying bold disks to their centers at a glance."""
    ax.add_patch(Circle(s.pos[i], s.rad[i],
                        facecolor=TYPE_FACE[s.typ[i]] if fill else "none",
                        edgecolor=edge, alpha=alpha, lw=lw, ls=ls, zorder=2))
    c = edge if accent else "k"
    ax.plot(*s.pos[i], "o", color=c, ms=4 if accent else 3,
            alpha=label_alpha, zorder=4)
    ax.annotate(s.name[i], s.pos[i], textcoords="offset points",
                xytext=LABEL_OFFSETS.get(s.name[i], (5, 5)), fontsize=10,
                color=c, alpha=label_alpha, zorder=5,
                fontweight="bold" if accent else "normal")

def _gray_edges(ax, s, dim=False):
    for i, j in itertools.combinations(range(s.n), 2):
        if s.adj[i][j]:
            ax.plot(*np.c_[s.pos[i], s.pos[j]], color="#999", lw=0.9,
                    alpha=.15 if dim else .6, zorder=3)

def _finish(fig, save):
    if save:
        fig.savefig(save, dpi=300, bbox_inches="tight")
    return fig


# --------------------------------------------------------------------------
# Chapter 3 — notation figures (unchanged behaviour, now module-level)
# --------------------------------------------------------------------------

def _draw(scene, title, emph=None, dim_others=False, edge_colors=None):
    s = scene
    emph = set(emph or [])
    fig, ax = _base_axes(s, figsize=(6.4, 5))
    for i in range(s.n):
        strong = (not dim_others) or (i in emph)
        ec = (edge_colors or {}).get(
            i, "#333" if i in emph else TYPE_EDGE[s.typ[i]])
        _disk(ax, s, i, ec, lw=2.6 if i in emph else 1.2,
              alpha=.85 if strong else .18, label_alpha=1 if strong else .3,
              accent=i in emph)
    for i, j in itertools.combinations(range(s.n), 2):
        if s.adj[i][j]:
            both = i in emph and j in emph
            ax.plot(*np.c_[s.pos[i], s.pos[j]],
                    color="#444" if both and emph else "#999",
                    lw=2.2 if both and emph else 0.9,
                    alpha=.9 if (both or not dim_others) else .15, zorder=3)
    ax.set_title(title, fontsize=11)
    fig.tight_layout()
    return fig


def fig_disk_graph(scene, save=None):
    return _finish(_draw(
        scene,
        r"$\mathcal{D}_2$: disk graph, $k=2$ radius types"
        "\n(blue = type-1 $(r_1)$, orange = type-2 $(r_2)$; gray = edges)"),
        save)


def fig_single_type_clique(scene, members=(0, 1, 2), save=None):
    return _finish(_draw(
        scene, r"$C_1$: a clique containing only type-1 disks",
        emph=list(members), dim_others=True), save)


def fig_max_clique(scene, save=None):
    return _finish(_draw(
        scene,
        r"$\mathcal{C}$: a maximum clique of $\mathcal{D}_2$"
        r" (here $|\mathcal{C}|=%d$)" % len(scene.cmax),
        emph=scene.cmax, dim_others=True), save)


def fig_type_classes(scene, save=None):
    colors = {**{i: TYPE_EDGE[1] for i in scene.c1},
              **{i: TYPE_EDGE[2] for i in scene.c2}}
    return _finish(_draw(
        scene,
        r"$\mathcal{C}_1,\ \mathcal{C}_2$: maximal same-type cliques"
        r" inside $\mathcal{C}$",
        emph=scene.cmax, dim_others=True, edge_colors=colors), save)


# --------------------------------------------------------------------------
# Chapter 3 — algorithm walk-through (storyboard S5-S7)
# --------------------------------------------------------------------------

def _shade_slabs(ax, a, alpha=.3):
    """Per-type slab shading: solid above the anchor segment, hatched below."""
    s = a.s
    (_, _), (ylo, yhi) = _limits(s)[0], _limits(s)[1]
    for t, (ai, bi) in a.guess.items():
        xa, xb = sorted((s.pos[ai][0], s.pos[bi][0]))
        xs = np.linspace(xa, xb, 60)
        ys = np.array([a.seg_y(t, x) for x in xs])
        ax.fill_between(xs, ys, yhi, color=TYPE_FACE[t], alpha=alpha, zorder=0)
        ax.fill_between(xs, ylo, ys, color=TYPE_FACE[t], alpha=alpha, zorder=0,
                        hatch="//", edgecolor="white", lw=0)
        for xw in (xa, xb):
            ax.plot([xw, xw], [ylo, yhi], color=TYPE_EDGE[t], ls="--",
                    lw=1.2, zorder=1)


def _slab_legend_patches():
    from matplotlib.patches import Patch
    return [Patch(facecolor="#d0d4da", alpha=.7,
                  label=r"upper slab $U_{a_ib_i}$"),
            Patch(facecolor="#d0d4da", alpha=.7, hatch="//",
                  edgecolor="white", label=r"lower slab $\overline{U}_{a_ib_i}$")]


def _draw_anchor_segments(ax, a):
    """Segments a_i b_i plus their labels, per guessed type."""
    s = a.s
    for t, (ai, bi) in a.guess.items():
        if ai != bi:
            ax.plot(*np.c_[s.pos[ai], s.pos[bi]], color=PSI_EDGE, lw=2.4,
                    zorder=4)

def _psi_legend(extra=()):
    items = [Line2D([], [], color=PSI_EDGE, lw=2.6,
                    label=r"guessed anchors $\Psi$")] + list(extra)
    return items


def fig_guess(ascene, save=None):
    """S5 — one iteration's guess: anchors of each type highlighted."""
    a, s = ascene, ascene.s
    fig, ax = _base_axes(s)
    for i in range(s.n):
        if i in a.psi:
            _disk(ax, s, i, PSI_EDGE, lw=3.0, accent=True)
        else:
            _disk(ax, s, i, TYPE_EDGE[s.typ[i]], alpha=.35, label_alpha=.6)
    _draw_anchor_segments(ax, a)
    names = {t: (s.name[ai], s.name[bi]) for t, (ai, bi) in a.guess.items()}
    ax.set_title(
        "One guess out of $O(n^{2k})$:  "
        + ",  ".join(rf"$(a_{t}, b_{t}) = ({p}, {q})$"
                     for t, (p, q) in sorted(names.items())),
        fontsize=11)
    ax.legend(handles=_psi_legend(), loc="lower left", fontsize=9)
    fig.tight_layout()
    return _finish(fig, save)


def fig_invalid_guess(scene, pair, save=None):
    """S5 companion — a hopeless guess: the two anchors don't even intersect,
    so Psi is not pairwise intersecting and the iteration is discarded."""
    s = scene
    i, j = pair
    fig, ax = _base_axes(s)
    for m in range(s.n):
        if m in (i, j):
            _disk(ax, s, m, "#e03131", lw=3.0, accent=True)
        else:
            _disk(ax, s, m, TYPE_EDGE[s.typ[m]], alpha=.3, label_alpha=.5)
    mid = (s.pos[i] + s.pos[j]) / 2
    ax.plot(*np.c_[s.pos[i], s.pos[j]], color="#e03131", lw=2, ls="--")
    ax.annotate("✗", mid, fontsize=22, color="#e03131",
                ha="center", va="center", zorder=6)
    ax.set_title(
        rf"A worthless guess: $({s.name[i]}, {s.name[j]})$ as $(a_1,b_1)$ — "
        "the disks don't intersect,\nso $\\Psi$ is not a clique and the "
        "iteration is discarded", fontsize=11)
    fig.tight_layout()
    return _finish(fig, save)


def fig_slabs(ascene, save=None):
    """S6 — the slabs of each guessed type, shaded above/below the segment."""
    a, s = ascene, ascene.s
    fig, ax = _base_axes(s)
    _shade_slabs(ax, a)
    for i in range(s.n):
        if i in a.psi:
            _disk(ax, s, i, PSI_EDGE, lw=3.0, alpha=.9, fill=False,
                  accent=True)
        else:
            _disk(ax, s, i, TYPE_EDGE[s.typ[i]], lw=1.2, alpha=.25,
                  label_alpha=.4, fill=False)
    _draw_anchor_segments(ax, a)
    ax.legend(handles=_psi_legend(_slab_legend_patches()),
              loc="lower left", fontsize=9)
    ax.set_title(
        r"Slabs of the guess: $U_{a_ib_i}$ (solid) and"
        r" $\overline{U}_{a_ib_i}$ (hatched), per type", fontsize=11)
    fig.tight_layout()
    return _finish(fig, save)


def fig_filter(ascene, save=None):
    """S7 — the filter: survivors form X (upper) and Y (lower); every other
    disk is discarded with its reason."""
    a, s = ascene, ascene.s
    fig, ax = _base_axes(s)
    _shade_slabs(ax, a, alpha=.18)
    for i in range(s.n):
        if i in a.psi:
            _disk(ax, s, i, PSI_EDGE, lw=3.0, accent=True)
        elif i in a.X:
            _disk(ax, s, i, X_EDGE, lw=3.0, accent=True)
        elif i in a.Y:
            _disk(ax, s, i, Y_EDGE, lw=3.0, accent=True)
        else:
            _disk(ax, s, i, "#adb5bd", lw=1.0, alpha=.10, label_alpha=.28)
            tag = "✗ slab" if a.reasons.get(i) == "slab" else "✗ misses $\\Psi$"
            ax.annotate(tag, s.pos[i], textcoords="offset points",
                        xytext=(0, -14), fontsize=8, ha="center",
                        color="#adb5bd", zorder=6)
    _draw_anchor_segments(ax, a)
    handles = _psi_legend((
        Line2D([], [], color=X_EDGE, lw=2.6,
               label=rf"$X$ = upper survivors  ({', '.join(s.name[i] for i in a.X)})"),
        Line2D([], [], color=Y_EDGE, lw=2.6,
               label=rf"$Y$ = lower survivors  ({', '.join(s.name[i] for i in a.Y)})"),
        *_slab_legend_patches(),
    ))
    ax.legend(handles=handles, loc="lower left", fontsize=9)
    ax.set_title(
        "The filter: keep a disk iff its center is in its type's slab\n"
        "AND it intersects every disk of $\\Psi$", fontsize=11)
    fig.tight_layout()
    return _finish(fig, save)


# --------------------------------------------------------------------------
# Chapter 3 — algorithm walk-through (storyboard S8-S11)
# --------------------------------------------------------------------------

def fig_x_clique(ascene, save=None):
    """S8 — Lemma 3.1 payoff: the upper camp X (with Psi) is one clique."""
    a, s = ascene, ascene.s
    fig, ax = _base_axes(s)
    camp = a.X + a.psi
    for i in range(s.n):
        if i in a.X:
            _disk(ax, s, i, X_EDGE, lw=3.0, accent=True)
        elif i in a.psi:
            _disk(ax, s, i, PSI_EDGE, lw=2.2, alpha=.55, fill=False)
        elif i in a.Y:
            # unbolded dashed preview of the lower camp, easing S7 -> S9
            _disk(ax, s, i, Y_EDGE, lw=1.6, alpha=.45, fill=False, ls="--",
                  label_alpha=.5)
        else:
            _disk(ax, s, i, "#adb5bd", lw=1.0, alpha=.12, label_alpha=.3)
    for i, j in itertools.combinations(camp, 2):
        both_x = i in a.X and j in a.X
        ax.plot(*np.c_[s.pos[i], s.pos[j]],
                color="#333" if both_x else "#aaa",
                lw=2.8 if both_x else 1.1,
                alpha=.95 if both_x else .6, zorder=3)
    handles = _psi_legend((
        Line2D([], [], color=X_EDGE, lw=2.6, label=r"$X$ = upper survivors"),
        Line2D([], [], color="#333", lw=2.8,
               label=r"adjacency within $X$ (Lemma 3.1)"),
        Line2D([], [], color="#aaa", lw=1.1,
               label=r"adjacency to $\Psi$ (by construction)"),
        Line2D([], [], color=Y_EDGE, lw=1.6, ls="--",
               label=r"$Y$ (up next)"),
    ))
    ax.legend(handles=handles, loc="lower left", fontsize=9)
    ax.set_title(
        "Lemma 3.1: the disks of $X$ are mutually adjacent —\n"
        "guaranteed for every guess", fontsize=11)
    fig.tight_layout()
    return _finish(fig, save)


def fig_missing_edges(ascene, save=None):
    """S9 — X ∪ Y is NOT a clique: the missing pairs cross the camps."""
    a, s = ascene, ascene.s
    fig, ax = _base_axes(s)
    for i in range(s.n):
        if i in a.X:
            _disk(ax, s, i, X_EDGE, lw=3.0, accent=True)
        elif i in a.Y:
            _disk(ax, s, i, Y_EDGE, lw=3.0, accent=True)
        elif i in a.psi:
            _disk(ax, s, i, PSI_EDGE, lw=2.2, alpha=.5, fill=False)
        else:
            _disk(ax, s, i, "#adb5bd", lw=1.0, alpha=.12, label_alpha=.3)
    cand = a.X + a.Y
    for i, j in itertools.combinations(cand, 2):
        if s.adj[i][j]:
            ax.plot(*np.c_[s.pos[i], s.pos[j]], color="#333", lw=2.2,
                    alpha=.9, zorder=3)
    for i, j in a.comp_edges:
        mid = (s.pos[i] + s.pos[j]) / 2
        ax.plot(*np.c_[s.pos[i], s.pos[j]], color="#e03131", lw=2.2,
                ls="--", zorder=3)
        ax.annotate("✗", mid, fontsize=20, color="#e03131",
                    ha="center", va="center", zorder=6)
    ax.set_title(
        "But $X \\cup Y$ is not a clique: pairs across the camps may miss\n"
        "(red dashed) — some disks of $X$ and $Y$ cannot coexist",
        fontsize=11)
    fig.tight_layout()
    return _finish(fig, save)


def _graph_panel(ax, ascene, edges, bold_edges=(), ring=(), title=""):
    """Abstract node-link panel: X stacked on the left, Y on the right."""
    a, s = ascene, ascene.s
    ys_x = np.linspace(1, -1, max(len(a.X), 1))
    ys_y = np.linspace(1, -1, max(len(a.Y), 1))
    P = {i: (-1.0, ys_x[k]) for k, i in enumerate(a.X)}
    P.update({i: (1.0, ys_y[k]) for k, i in enumerate(a.Y)})
    for i, j in edges:
        bold = (i, j) in bold_edges or (j, i) in bold_edges
        ax.plot(*np.c_[P[i], P[j]], color="#e03131" if bold else "#555",
                lw=3.2 if bold else 1.6, zorder=2)
    for i, xy in P.items():
        col = X_EDGE if i in a.X else Y_EDGE
        ax.plot(*xy, "o", ms=16, color=col, zorder=3)
        if i in ring:
            ax.plot(*xy, "o", ms=26, mfc="none", mec=PSI_EDGE, mew=2.5,
                    zorder=4)
        ax.annotate(s.name[i], xy, textcoords="offset points",
                    xytext=(0, 16), ha="center", fontsize=11, zorder=5)
    ax.set_title(title, fontsize=11)
    ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.7, 1.7)
    ax.set_aspect("equal"); ax.axis("off")


def fig_complement(ascene, save=None):
    """S10 — the candidate graph vs its complement H; matching + selection."""
    a, s = ascene, ascene.s
    cand = a.X + a.Y
    adj_edges = [(i, j) for i, j in itertools.combinations(cand, 2)
                 if s.adj[i][j]]
    fig, (axl, axr) = plt.subplots(1, 2, figsize=(10.5, 5))
    _graph_panel(axl, a, adj_edges,
                 title="candidate graph on $X \\cup Y$\n"
                       "(max clique = what we want)")
    _graph_panel(axr, a, a.comp_edges, bold_edges=a.matching, ring=a.chosen,
                 title="complement $H$ — bipartite!\n"
                       "(bold: max matching; ringed: max independent set)")
    kx = len(cand) - len(a.matching)
    fig.suptitle(
        rf"Kőnig: $\alpha(H) = |X \cup Y| - $ matching $= {len(cand)} - "
        rf"{len(a.matching)} = {kx}$  →  chosen: "
        + "{" + ", ".join(s.name[i] for i in a.chosen) + "}",
        fontsize=12)
    fig.tight_layout()
    return _finish(fig, save)


def fig_assembly(ascene, save=None):
    """S11 — assembly: Psi ∪ (selected disks) is the iteration's output."""
    a, s = ascene, ascene.s
    fig, ax = _base_axes(s)
    for i in range(s.n):
        if i in a.final:
            edge = PSI_EDGE if i in a.psi else (
                X_EDGE if i in a.X else Y_EDGE)
            _disk(ax, s, i, edge, lw=3.0, accent=True)
        else:
            _disk(ax, s, i, "#adb5bd", lw=1.0, alpha=.12, label_alpha=.3)
    for i, j in itertools.combinations(a.final, 2):
        ax.plot(*np.c_[s.pos[i], s.pos[j]], color="#333", lw=1.8,
                alpha=.85, zorder=3)
    ax.set_title(
        rf"Output of this iteration: $\Psi \cup$ selected disks — a clique of"
        rf" size {len(a.final)}"
        "\n(the algorithm returns the max over all $O(n^{2k})$ guesses)",
        fontsize=11)
    fig.tight_layout()
    return _finish(fig, save)
