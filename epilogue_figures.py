# epilogue_figures.py — the "if time permits" act: CCJ's lens-based recipe
# (paper Section 4 overview) and why it breaks for two radii (Section 6.1).
#
# Reuses the Act II color grammar from scene_figures so the epilogue visually
# rhymes with the algorithm walk-through:
#   green = guessed disks, violet = upper camp, magenta = lower camp,
#   red dashed = missing adjacency.

import itertools

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

from scene_figures import PSI_EDGE, X_EDGE, Y_EDGE, TYPE_FACE, TYPE_EDGE


def _lens_outline(c1, c2, R, samples=120):
    """Boundary polygon of the intersection of two radius-R disks."""
    c1, c2 = np.asarray(c1, float), np.asarray(c2, float)
    d = np.linalg.norm(c2 - c1)
    alpha = np.arccos(d / (2 * R))          # half-opening of each arc
    base1 = np.arctan2(*(c2 - c1)[::-1])
    base2 = np.arctan2(*(c1 - c2)[::-1])
    t = np.linspace(-alpha, alpha, samples)
    arc1 = c1 + R * np.c_[np.cos(base1 + t), np.sin(base1 + t)]
    arc2 = c2 + R * np.c_[np.cos(base2 + t), np.sin(base2 + t)]
    return np.vstack([arc1, arc2])


def _finish(fig, save):
    if save:
        fig.savefig(save, dpi=300, bbox_inches="tight")
    return fig


# --------------------------------------------------------------------------
# S3 — the CCJ (1990) recipe on unit disks
# --------------------------------------------------------------------------

def fig_ccj_lens(save=None):
    """Guess the farthest pair (v, w); every other clique member's center
    lies in the lens of radius |vw|; the line through v, w splits the lens
    into two camps that are each automatically a clique."""
    R = 1.0                                   # unit disks: adjacent iff dist<=2
    v, w = np.array([0.0, 0.0]), np.array([1.8, 0.0])
    d = np.linalg.norm(w - v)
    upper = [np.array(p) for p in [(0.9, 0.7), (0.5, 0.35), (0.9, 1.5)]]
    lower = [np.array(p) for p in [(1.0, -0.45), (0.9, -1.5)]]
    pts = {"v": v, "w": w}
    pts.update({f"x{k+1}": p for k, p in enumerate(upper)})
    pts.update({f"y{k+1}": p for k, p in enumerate(lower)})

    # honesty checks: everyone in the lens; same-half pairs adjacent
    for name, p in pts.items():
        assert np.linalg.norm(p - v) <= d + 1e-9, name
        assert np.linalg.norm(p - w) <= d + 1e-9, name
    for A in (upper, lower):
        for p, q in itertools.combinations(A, 2):
            assert np.linalg.norm(p - q) <= 2 * R + 1e-9

    fig, ax = plt.subplots(figsize=(8.2, 6.4))
    lens = _lens_outline(v, w, d)
    ax.fill(*lens.T, color="#dee2e6", alpha=.7, zorder=0)
    ax.plot(*lens.T, color="#868e96", lw=1.2, zorder=1)
    ax.plot([v[0] - 1.3, w[0] + 1.3], [0, 0], color="k", ls="-.",
            lw=1.2, alpha=.7, zorder=2)

    def point(p, name, color, bold=True):
        ax.add_patch(Circle(p, R, facecolor="none", edgecolor=color,
                            alpha=.35, lw=1.2, zorder=1))
        ax.plot(*p, "o", ms=7, color=color, zorder=5)
        ax.annotate(name, p, textcoords="offset points", xytext=(6, 6),
                    fontsize=11, color=color,
                    fontweight="bold" if bold else "normal", zorder=6)

    point(v, "v", PSI_EDGE); point(w, "w", PSI_EDGE)
    ax.plot(*np.c_[v, w], color=PSI_EDGE, lw=2.4, zorder=4)
    for k, p in enumerate(upper):
        point(p, f"x{k+1}", X_EDGE)
    for k, p in enumerate(lower):
        point(p, f"y{k+1}", Y_EDGE)

    for p, q in itertools.combinations(upper, 2):
        ax.plot(*np.c_[p, q], color="#333", lw=2.0, alpha=.9, zorder=3)
    for p, q in itertools.combinations(lower, 2):
        ax.plot(*np.c_[p, q], color="#333", lw=2.0, alpha=.9, zorder=3)
    for p in upper:
        for q in lower:
            if np.linalg.norm(p - q) <= 2 * R:
                ax.plot(*np.c_[p, q], color="#aaa", lw=1.1, alpha=.6,
                        zorder=2)
            else:
                ax.plot(*np.c_[p, q], color="#e03131", lw=1.8, ls="--",
                        zorder=3)
    missing = [(p, q) for p in upper for q in lower
               if np.linalg.norm(p - q) > 2 * R]
    worst = max(missing, key=lambda e: np.linalg.norm(e[0] - e[1]))
    ax.annotate("✗", (worst[0] + worst[1]) / 2, fontsize=18, color="#e03131",
                ha="center", va="center", zorder=6)

    handles = [
        Line2D([], [], color=PSI_EDGE, lw=2.4,
               label="guessed farthest pair $(v, w)$"),
        Line2D([], [], color="#333", lw=2.0, label="within a half: adjacent,"
               " guaranteed"),
        Line2D([], [], color="#aaa", lw=1.1, label="across halves: sometimes"),
        Line2D([], [], color="#e03131", lw=1.8, ls="--",
               label="across halves: sometimes not → matching"),
    ]
    ax.legend(handles=handles, loc="lower left", fontsize=9)
    ax.set_title(
        "CCJ 1990, unit disks: centers adjacent to both $v, w$ lie in the"
        " lens of radius $|vw|$;\nthe line $\\ell_{vw}$ splits it into two"
        " cliques — same skeleton, lens instead of slab", fontsize=11)
    ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout()
    return _finish(fig, save)


# --------------------------------------------------------------------------
# S4 — the deception: the same recipe with two radii
# --------------------------------------------------------------------------

def fig_lens_deception(save=None):
    """Two radii: guessing the farthest SMALL pair (p, q) confines small
    centers to a small lens L_s and big centers to a big lens L_b — but the
    line through p, q no longer splits L_b into cliques: two big disks on the
    SAME side can miss each other."""
    rs, rb = 0.5, 1.2
    p, q = np.array([-0.3, 0.0]), np.array([0.3, 0.0])
    dpq = np.linalg.norm(q - p)               # farthest small pair: <= 2*rs
    assert dpq <= 2 * rs
    u1, u2 = np.array([-1.30, 0.55]), np.array([1.30, 0.55])

    # honesty checks: u1, u2 are legal big disks (intersect both guessed
    # small disks), sit on the same side of l_pq, yet do NOT intersect
    for u in (u1, u2):
        assert np.linalg.norm(u - p) <= rs + rb + 1e-9
        assert np.linalg.norm(u - q) <= rs + rb + 1e-9
    assert u1[1] > 0 and u2[1] > 0
    assert np.linalg.norm(u1 - u2) > 2 * rb + 1e-9

    sm = np.array([0.0, 0.15])                # an innocent small disk in L_s

    fig, ax = plt.subplots(figsize=(9.4, 6.6))
    Lb = _lens_outline(p, q, rs + rb)
    Ls = _lens_outline(p, q, dpq)
    ax.fill(*Lb.T, color=TYPE_FACE[2], alpha=.30, zorder=0)
    ax.plot(*Lb.T, color=TYPE_EDGE[2], lw=1.4, zorder=1)
    ax.fill(*Ls.T, color=TYPE_FACE[1], alpha=.75, zorder=1)
    ax.plot(*Ls.T, color=TYPE_EDGE[1], lw=1.4, zorder=2)
    ax.annotate("$L_b$: possible big-disk centers", (0, 1.55),
                fontsize=11, ha="center", color=TYPE_EDGE[2])
    ax.annotate("$L_s$: possible small-disk centers", xy=(-0.28, -0.35),
                xytext=(-2.55, -1.15), fontsize=11, color=TYPE_EDGE[1],
                arrowprops=dict(arrowstyle="->", color=TYPE_EDGE[1], lw=1.2))
    ax.plot([-2.7, 2.7], [0, 0], color="k", ls="-.", lw=1.2, alpha=.7,
            zorder=2)
    ax.annotate(r"$\ell_{pq}$", (-2.65, 0.07), fontsize=11)

    # the guessed small pair
    for c, name, dx in ((p, "p", -14), (q, "q", 8)):
        ax.add_patch(Circle(c, rs, facecolor="none", edgecolor=PSI_EDGE,
                            lw=2.4, zorder=3))
        ax.plot(*c, "o", ms=6, color=PSI_EDGE, zorder=5)
        ax.annotate(name, c, textcoords="offset points", xytext=(dx, 6),
                    fontsize=12, color=PSI_EDGE, fontweight="bold", zorder=6)
    # an innocent small disk (upper half of L_s: all fine there)
    ax.add_patch(Circle(sm, rs, facecolor=TYPE_FACE[1], edgecolor=TYPE_EDGE[1],
                        alpha=.5, lw=1.4, zorder=3))
    ax.plot(*sm, "o", ms=5, color=TYPE_EDGE[1], zorder=5)

    # the two same-side big disks that miss each other
    for u, name in ((u1, "$u_1$"), (u2, "$u_2$")):
        ax.add_patch(Circle(u, rb, facecolor=TYPE_FACE[2],
                            edgecolor=TYPE_EDGE[2], alpha=.55, lw=2.4,
                            zorder=3))
        ax.plot(*u, "o", ms=7, color=TYPE_EDGE[2], zorder=5)
        ax.annotate(name, u, textcoords="offset points", xytext=(6, 8),
                    fontsize=12, color=TYPE_EDGE[2], fontweight="bold",
                    zorder=6)
    mid = (u1 + u2) / 2
    ax.plot(*np.c_[u1, u2], color="#e03131", lw=2.2, ls="--", zorder=4)
    ax.annotate("✗", mid + (0, 0.14), fontsize=20, color="#e03131",
                ha="center", va="center", zorder=6)
    ax.annotate(r"$|u_1u_2| > 2r_b$: same side, yet NOT adjacent",
                mid + (0, 0.40), fontsize=11, color="#e03131", ha="center",
                zorder=6)

    ax.set_title(
        "Two radii, same recipe: big-disk centers land in the bigger lens"
        " $L_b$ —\nbut $u_1, u_2$ are on the SAME side of $\\ell_{pq}$ and"
        " their disks do not intersect: the split no longer forces cliques",
        fontsize=11)
    ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout()
    return _finish(fig, save)
