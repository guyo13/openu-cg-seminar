# Lemma 2.1 "sliding" visualization — paste this whole block into one marimo cell.
# It writes two GIFs next to your notebook:
#   lemma21_case_b.gif  — exit point o slides ALONG ab, away from m, toward an endpoint
#   lemma21_case_c.gif  — exit point o slides DOWN the vertical slab wall, toward an endpoint
# In a following marimo cell you can display them with:  mo.image(src="lemma21_case_b.gif")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# ---------- geometry helpers ----------

def foot_of_perpendicular(p, a, b):
    """Foot m of the perpendicular from p onto line l_ab (as parameter t along a->b)."""
    ab = b - a
    t = np.dot(p - a, ab) / np.dot(ab, ab)
    return t, a + t * ab

def ray_hit_segment(p, q, a, b):
    """Intersection of ray p->q (beyond q) with line l_ab; returns (s, t, point)."""
    d, ab = q - p, b - a
    A = np.array([[d[0], -ab[0]], [d[1], -ab[1]]])
    s, t = np.linalg.solve(A, a - p)
    return s, t, p + s * d

def ray_hit_vertical(p, q, x_wall):
    """Intersection of ray p->q with the vertical line x = x_wall."""
    d = q - p
    s = (x_wall - p[0]) / d[0]
    return s, p + s * d

# ---------- one reusable animator ----------

def animate_case(p, q, a, b, case, fname, frames=70, hold=18):
    """case='b': o slides along ab away from m.  case='c': o slides down a wall."""
    slab_top = max(p[1], q[1], a[1], b[1]) + 1.2
    xa, xb = a[0], b[0]

    # exit point o of the ray p->q out of the slab region, and the slide path
    if case == "b":
        s, t_o, o0 = ray_hit_segment(p, q, a, b)
        t_m, m = foot_of_perpendicular(p, a, b)
        t_end = 1.0 if t_o >= t_m else 0.0          # away from m -> endpoint
        path = [a + (t_o + (t_end - t_o) * u) * (b - a)
                for u in np.linspace(0, 1, frames)]
        target = b if t_end == 1.0 else a
        subtitle = "o slides along ab, AWAY from m  →  |po| grows"
    elif case == "c":
        wall = xa if q[0] < p[0] else xb            # wall the ray exits through
        s, o0 = ray_hit_vertical(p, q, wall)
        y_end = a[1] if wall == xa else b[1]
        path = [np.array([wall, o0[1] + (y_end - o0[1]) * u])
                for u in np.linspace(0, 1, frames)]
        target = a if wall == xa else b
        m = np.array([wall, p[1]])   # closest point of the wall line to p
        subtitle = "o slides DOWN the slab wall  →  |po| grows"
    elif case == "v":
        # Scenario 2: a and b share an x-coordinate; the slab degenerates
        # to the vertical line through them, and q lies on that line.
        bottom = a if a[1] <= b[1] else b
        path = [np.array([xa, q[1] + (bottom[1] - q[1]) * u])
                for u in np.linspace(0, 1, frames)]
        target = bottom
        m = np.array([xa, p[1]])     # closest point of the line to p
        subtitle = "vertical ab: o slides down to the LOWER endpoint"

    fig, ax = plt.subplots(figsize=(7, 5.2))
    ax.set_aspect("equal")
    pad = 1.0
    ax.set_xlim(min(xa, p[0]) - pad, max(xb, p[0]) + pad)
    ax.set_ylim(min(a[1], b[1]) - 1.0, slab_top + 0.4)
    ax.axis("off")

    # static scenery: slab, segment ab, anchors, p, q, reference distances |pa|,|pb|
    if abs(xb - xa) > 1e-9:
        upper = np.array([[xa, a[1]], [xb, b[1]], [xb, slab_top], [xa, slab_top]])
        ax.fill(*upper.T, color="#cfe3ff", alpha=.55, zorder=0,
                label="upper slab $U_{ab}$")
        ax.plot([xa, xa], [a[1], slab_top], color="#5a8fd6", lw=1.4)
        ax.plot([xb, xb], [b[1], slab_top], color="#5a8fd6", lw=1.4)
    else:  # degenerate: the slab IS the vertical line above the segment
        top_y = max(a[1], b[1])
        ax.plot([xa, xa], [top_y, slab_top], color="#cfe3ff", lw=7,
                solid_capstyle="butt", zorder=0)
        ax.plot([xa, xa], [top_y, slab_top], color="#5a8fd6", lw=1.2, zorder=1)
    ax.plot(*np.c_[a, b], color="k", lw=2.2)
    for pt, name, dy in [(a, "a", -.35), (b, "b", -.35), (p, "p", .25), (q, "q", .25)]:
        ax.plot(*pt, "o", color="#d9480f" if name == "p" else "k", ms=7, zorder=5)
        ax.annotate(name, pt, textcoords="offset points", xytext=(6, 14 * dy),
                    fontsize=14, fontstyle="italic")
    for anchor in (a, b):                            # the two "worst case" distances
        ax.plot(*np.c_[p, anchor], ls=":", color="#888", lw=1.3)
    ax.plot(*np.c_[p, m], ls="--", color="#2b8a3e", lw=1.5)   # pm, dashed green
    ax.plot(*m, "s", color="#2b8a3e", ms=6, zorder=5)
    ax.annotate("m", m, textcoords="offset points", xytext=(6, -16),
                fontsize=13, fontstyle="italic", color="#2b8a3e")

    ax.set_title("Lemma 2.1 — " + subtitle, fontsize=12)

    # dynamic artists
    ray_ln,  = ax.plot([], [], "--", color="#d9480f", lw=1.6)     # ray p->o
    po_ln,   = ax.plot([], [], "-",  color="#d9480f", lw=2.4)     # segment po
    o_dot,   = ax.plot([], [], "o",  color="#d9480f", ms=8, zorder=6)
    o_lbl    = ax.text(0, 0, "", fontsize=13, fontstyle="italic",
                       color="#d9480f", zorder=6)
    readout  = ax.text(.02, .99, "", transform=ax.transAxes, fontsize=11,
                       va="top", family="monospace")

    dmax = max(np.linalg.norm(p - a), np.linalg.norm(p - b))
    seq = path + [path[-1]] * hold                  # freeze on the final frame

    def draw(i):
        o = seq[i]
        po_ln.set_data(*np.c_[p, o])
        ray_ln.set_data(*np.c_[p, q, o])
        o_dot.set_data([o[0]], [o[1]])
        o_lbl.set_position((o[0] + 0.14, o[1] + 0.14))
        o_lbl.set_text("o")
        d = np.linalg.norm(p - o)
        done = i >= frames - 1
        readout.set_text(f"|po| = {d:4.2f}   max(|pa|,|pb|) = {dmax:4.2f}"
                         + ("\n✓ |pq| ≤ |po| ≤ max(|pa|,|pb|)" if done else ""))
        o_dot.set_color("#2b8a3e" if done else "#d9480f")
        o_lbl.set_color("#2b8a3e" if done else "#d9480f")
        return po_ln, ray_ln, o_dot, o_lbl, readout

    anim = FuncAnimation(fig, draw, frames=len(seq), interval=45, blit=True)
    anim.save(fname, writer=PillowWriter(fps=22))
    plt.close(fig)
    return fname

# ---------- the two scenarios of Figure 1(b)-(c) ----------

a, b = np.array([0.0, 0.0]), np.array([4.0, 0.8])

# Case (b): p high above the slab; the ray p->q exits through segment ab itself
animate_case(p=np.array([1.1, 3.4]), q=np.array([2.1, 1.2]),
             a=a, b=b, case="b", fname="lemma21_case_b.gif")

# Case (c): p outside the slab to the right; the ray exits through the LEFT wall
animate_case(p=np.array([5.3, 2.4]), q=np.array([3.2, 2.0]),
             a=a, b=b, case="c", fname="lemma21_case_c.gif")

# Scenario 2 (degenerate): a and b share the same x-coordinate; the slab
# collapses to the vertical line through them, and q sits on that line.
av, bv = np.array([2.0, 0.0]), np.array([2.0, 1.6])
animate_case(p=np.array([3.7, 3.0]), q=np.array([2.0, 2.35]),
             a=av, b=bv, case="v", fname="lemma21_case_vertical.gif")

print("wrote lemma21_case_b.gif, lemma21_case_c.gif and lemma21_case_vertical.gif")
