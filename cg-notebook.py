import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():

    import itertools
    from types import SimpleNamespace
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Polygon, Circle
    import math

    TYPE_FACE = {1: "#a5d8ff", 2: "#ffd8a8"}      # fill by radius type
    TYPE_EDGE = {1: "#1971c2", 2: "#e8590c"}
    return (
        Circle,
        Polygon,
        SimpleNamespace,
        TYPE_EDGE,
        TYPE_FACE,
        itertools,
        math,
        np,
        plt,
    )


@app.cell
def _(Circle, Polygon, math, np, plt):
    def lens_geometry():

        # Constants
        d = 1.0
        u_x, u_y = -d/2, 0
        v_x, v_y = d/2, 0
        p_x, p_y = 0, math.sqrt(d**2 - (d/2)**2)

        fig, ax = plt.subplots(figsize=(8, 8))

        # Draw the two circles with radius d
        circle_u = Circle((u_x, u_y), d, color='blue', fill=False, linestyle='--', alpha=0.4)
        circle_v = Circle((v_x, v_y), d, color='red', fill=False, linestyle='--', alpha=0.4)
        ax.add_patch(circle_u)
        ax.add_patch(circle_v)

        # Generate points for the top lens (Blue area)
        # Angles for arc centered at u (from v to P)
        angles_u_top = np.linspace(0, np.pi/3, 100)
        arc_u_x_top = u_x + d * np.cos(angles_u_top)
        arc_u_y_top = u_y + d * np.sin(angles_u_top)

        # Angles for arc centered at v (from P to u)
        angles_v_top = np.linspace(2*np.pi/3, np.pi, 100)
        arc_v_x_top = v_x + d * np.cos(angles_v_top)
        arc_v_y_top = v_y + d * np.sin(angles_v_top)

        top_lens_x = np.concatenate([arc_u_x_top, arc_v_x_top])
        top_lens_y = np.concatenate([arc_u_y_top, arc_v_y_top])
        ax.fill(top_lens_x, top_lens_y, color='skyblue', alpha=0.5, label='Top Half (Clique 1)')

        # Generate points for the bottom lens (Red area)
        angles_u_bottom = np.linspace(0, -np.pi/3, 100)
        arc_u_x_bottom = u_x + d * np.cos(angles_u_bottom)
        arc_u_y_bottom = u_y + d * np.sin(angles_u_bottom)

        angles_v_bottom = np.linspace(-2*np.pi/3, -np.pi, 100)
        arc_v_x_bottom = v_x + d * np.cos(angles_v_bottom)
        arc_v_y_bottom = v_y + d * np.sin(angles_v_bottom)

        bottom_lens_x = np.concatenate([arc_u_x_bottom, arc_v_x_bottom])
        bottom_lens_y = np.concatenate([arc_u_y_bottom, arc_v_y_bottom])
        ax.fill(bottom_lens_x, bottom_lens_y, color='lightcoral', alpha=0.5, label='Bottom Half (Clique 2)')

        # Draw Equilateral Triangle
        triangle = Polygon([[u_x, u_y], [v_x, v_y], [p_x, p_y]], closed=True, fill=False, edgecolor='black', linewidth=2.5, zorder=5)
        ax.add_patch(triangle)

        # Draw dividing line
        ax.plot([-1.2, 1.2], [0, 0], color='black', linestyle='-.', zorder=4, alpha=0.7)

        # Plot points u, v, P
        ax.scatter([u_x, v_x, p_x], [u_y, v_y, p_y], color='black', zorder=6, s=80)

        # Annotations
        ax.text(u_x - 0.12, u_y - 0.1, 'u', fontsize=16, fontweight='bold')
        ax.text(v_x + 0.12, v_y - 0.1, 'v', fontsize=16, fontweight='bold')
        ax.text(p_x, p_y + 0.08, 'P', fontsize=16, fontweight='bold', ha='center')

        # Distance labels for the triangle edges
        ax.text(0, -0.08, 'd', fontsize=14, ha='center', va='top', fontweight='bold')
        ax.text(-0.35, 0.45, 'd', fontsize=14, ha='right', fontweight='bold')
        ax.text(0.35, 0.45, 'd', fontsize=14, ha='left', fontweight='bold')

        # Setup plot limits and display
        ax.set_aspect('equal')
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.2, 1.6)
        ax.axis('off')
        plt.legend(loc='upper right', fontsize=12)
        plt.title('The Co-Bipartite Lens Region', fontsize=16, fontweight='bold')

        plt.tight_layout()
        plt.savefig('lens_geometry.png', dpi=300)
        return fig

    return (lens_geometry,)


@app.cell
def _(lens_geometry):
    lens_geometry()
    return


@app.cell
def _(plt):
    def slab_geom():
        # Coordinates for points a and b
        a_x, a_y = 1, 2
        b_x, b_y = 6, 4

        y_max = 7
        y_min = 0

        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot the line segment ab
        ax.plot([a_x, b_x], [a_y, b_y], color='black', linewidth=2.5, zorder=4)
        ax.scatter([a_x, b_x], [a_y, b_y], color='black', s=80, zorder=5)

        # Plot the vertical bounding lines l_a^v and l_b^v
        ax.axvline(x=a_x, color='gray', linestyle='--', linewidth=1.5, zorder=2)
        ax.axvline(x=b_x, color='gray', linestyle='--', linewidth=1.5, zorder=2)

        # Fill the Upper Slab U_ab
        ax.fill_between([a_x, b_x], [a_y, b_y], y_max, color='skyblue', alpha=0.5, label='Upper Slab ($U_{ab}$)', zorder=1)

        # Fill the Lower Slab \overline{U}_ab
        ax.fill_between([a_x, b_x], y_min, [a_y, b_y], color='lightcoral', alpha=0.5, label='Lower Slab ($\\overline{U}_{ab}$)', zorder=1)

        # Annotations
        ax.text(a_x - 0.2, a_y, 'a', fontsize=16, fontweight='bold', ha='right')
        ax.text(b_x + 0.2, b_y, 'b', fontsize=16, fontweight='bold', ha='left')
        ax.text(a_x, y_max - 0.5, ' $l_a^v$', fontsize=14, color='gray')
        ax.text(b_x, y_max - 0.5, ' $l_b^v$', fontsize=14, color='gray')
        ax.text((a_x + b_x)/2, (a_y + b_y)/2 + 1.5, '$U_{ab}$ (Upper Slab)', fontsize=14, fontweight='bold', ha='center')
        ax.text((a_x + b_x)/2, (a_y + b_y)/2 - 1.5, '$\\overline{U}_{ab}$ (Lower Slab)', fontsize=14, fontweight='bold', ha='center')

        # Setup plot limits and display
        ax.set_xlim(a_x - 2, b_x + 2)
        ax.set_ylim(y_min, y_max)
        ax.axis('off')
        ax.legend(loc='upper left', fontsize=12)
        plt.title('The Slab-Based Regions', fontsize=16, fontweight='bold')

        plt.tight_layout()
        plt.savefig('slab_geometry.png', dpi=300)
        return fig


    return (slab_geom,)


@app.cell
def _(slab_geom):
    slab_geom()
    return


@app.cell
def _():
    # def notation_drawings():
    #     # Section 3 notation, visualized — paste this whole block into one marimo cell.
    #     # Writes section3_notation.png (for your slides) and shows the figure inline.
    #     # The maximum clique is computed by brute force from the actual geometry,
    #     # so every highlighted set is provably correct for this arrangement.

    #     import itertools
    #     import numpy as np
    #     import matplotlib.pyplot as plt
    #     from matplotlib.patches import Circle

    #     # ---------- a concrete D_2 : two radius types (k = 2) ----------
    #     R1, R2 = 0.8, 1.4                       # r_1 < r_2
    #     disks = [  # (x,     y,    radius, name)
    #         ( 0.0,  0.0, R1, "s1"),
    #         ( 1.1,  0.2, R1, "s2"),
    #         ( 0.5,  0.9, R1, "s3"),
    #         ( 2.6, -0.5, R1, "s4"),
    #         (-1.6, -1.4, R1, "s5"),
    #         ( 1.8,  1.2, R2, "b1"),
    #         ( 0.9, -1.0, R2, "b2"),
    #         (-2.4,  0.6, R2, "b3"),
    #     ]
    #     pos  = np.array([[d[0], d[1]] for d in disks])
    #     rad  = np.array([d[2] for d in disks])
    #     name = [d[3] for d in disks]
    #     n    = len(disks)
    #     typ  = [1 if r == R1 else 2 for r in rad]

    #     # adjacency: disks intersect  <=>  |ab| <= r_a + r_b
    #     A = [[i != j and np.linalg.norm(pos[i] - pos[j]) <= rad[i] + rad[j] + 1e-12
    #           for j in range(n)] for i in range(n)]

    #     def is_clique(S):
    #         return all(A[i][j] for i, j in itertools.combinations(S, 2))

    #     # brute-force maximum clique (n is tiny, so this is instant and exact)
    #     Cmax = max((S for m in range(n, 0, -1)
    #                 for S in itertools.combinations(range(n), m) if is_clique(S)),
    #                key=len)
    #     C1 = [i for i in Cmax if typ[i] == 1]    # calligraphic C_1: type-1 disks of C
    #     C2 = [i for i in Cmax if typ[i] == 2]    # calligraphic C_2: type-2 disks of C
    #     print("maximum clique C =", [name[i] for i in Cmax],
    #           "| C_1 =", [name[i] for i in C1], "| C_2 =", [name[i] for i in C2])

    #     TYPE_FACE = {1: "#a5d8ff", 2: "#ffd8a8"}          # fill by radius type
    #     TYPE_EDGE = {1: "#1971c2", 2: "#e8590c"}

    #     def draw(ax, title, emph=None, dim_others=False, edge_colors=None):
    #         """Draw the arrangement; emph = set of indices to bold, others optionally faded."""
    #         emph = set(emph or [])
    #         for i in range(n):
    #             strong = (not dim_others) or (i in emph)
    #             ec = (edge_colors or {}).get(i, "#333" if i in emph else TYPE_EDGE[typ[i]])
    #             ax.add_patch(Circle(pos[i], rad[i],
    #                                 facecolor=TYPE_FACE[typ[i]],
    #                                 edgecolor=ec,
    #                                 alpha=.85 if strong else .18,
    #                                 lw=2.6 if i in emph else 1.2, zorder=2))
    #             ax.plot(*pos[i], "o", color="k", ms=3,
    #                     alpha=1 if strong else .25, zorder=4)
    #             ax.annotate(name[i], pos[i], textcoords="offset points", xytext=(5, 5),
    #                         fontsize=9, alpha=1 if strong else .3, zorder=5)
    #         # intersection-graph edges between centers
    #         for i, j in itertools.combinations(range(n), 2):
    #             if A[i][j]:
    #                 both = i in emph and j in emph
    #                 ax.plot(*np.c_[pos[i], pos[j]],
    #                         color="#444" if both and emph else "#999",
    #                         lw=2.2 if both and emph else 0.9,
    #                         alpha=.9 if (both or not dim_others) else .15, zorder=3)
    #         ax.set_title(title, fontsize=11)
    #         ax.set_aspect("equal"); ax.set_xlim(-4.1, 4.3); ax.set_ylim(-3.1, 3.1)
    #         ax.axis("off")

    #     fig, axes = plt.subplots(2, 2, figsize=(12, 8.6))

    #     # (a) the disk graph itself
    #     draw(axes[0, 0],
    #          r"$\mathcal{D}_2$: disk graph, $k=2$ radius types"
    #          "\n(blue = type-1 $(r_1)$, orange = type-2 $(r_2)$; gray = edges)")

    #     # (b) a clique made of one type only
    #     draw(axes[0, 1],
    #          r"$C_1$: a clique containing only type-1 disks",
    #          emph=[0, 1, 2], dim_others=True)

    #     # (c) the maximum clique
    #     draw(axes[1, 0],
    #          r"$\mathcal{C}$: a maximum clique of $\mathcal{D}_2$ (here $|\mathcal{C}|=%d$)"
    #          % len(Cmax),
    #          emph=Cmax, dim_others=True)

    #     # (d) the type classes inside the maximum clique
    #     draw(axes[1, 1],
    #          r"$\mathcal{C}_1,\ \mathcal{C}_2$: maximal same-type cliques inside $\mathcal{C}$",
    #          emph=Cmax, dim_others=True,
    #          edge_colors={**{i: TYPE_EDGE[1] for i in C1},
    #                       **{i: TYPE_EDGE[2] for i in C2}})

    #     fig.suptitle("Section 3 notation on one arrangement of disks", fontsize=13)
    #     fig.tight_layout()
    #     fig.savefig("section3_notation.png", dpi=160, bbox_inches="tight")
    #     return fig   # last expression -> marimo renders it inline

    # notation_drawings()
    return


@app.cell
def _(Circle, SimpleNamespace, TYPE_EDGE, TYPE_FACE, itertools, np, plt):
    # Section 3 notation, visualized — function-per-figure edition for marimo.
    #
    # Paste this block into ONE cell (it only defines functions), then render each
    # figure in its own cell:
    #
    #     scene = make_scene()
    #     fig_disk_graph(scene)                 # D_k
    #     fig_single_type_clique(scene)         # C_1
    #     fig_max_clique(scene)                 # calligraphic C
    #     fig_type_classes(scene)               # calligraphic C_1, C_2
    #
    # Each fig_* function returns a matplotlib Figure (marimo renders it if it's
    # the cell's last expression) and accepts save="filename.png" to export.

    def make_scene(r1=0.8, r2=1.4):
        """Build the example D_2 arrangement; compute adjacency and the exact
        maximum clique (brute force on the geometry). Returns a SimpleNamespace
        holding everything the drawing functions need."""
        disks = [  # (x,     y,    radius, name)
            ( 0.0,  0.0, r1, "s1"),
            ( 1.1,  0.2, r1, "s2"),
            ( 0.5,  0.9, r1, "s3"),
            ( 2.6, -0.5, r1, "s4"),
            (-1.6, -1.4, r1, "s5"),
            ( 1.8,  1.2, r2, "b1"),
            ( 0.9, -1.0, r2, "b2"),
            (-2.4,  0.6, r2, "b3"),
        ]
        pos = np.array([[d[0], d[1]] for d in disks])
        rad = np.array([d[2] for d in disks])
        nam = [d[3] for d in disks]
        n = len(disks)
        typ = [1 if r == r1 else 2 for r in rad]

        # disks intersect  <=>  |ab| <= r_a + r_b
        adj = [[i != j and np.linalg.norm(pos[i] - pos[j]) <= rad[i] + rad[j] + 1e-12
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


    def _draw(scene, title, emph=None, dim_others=False, edge_colors=None):
        """Shared renderer: one arrangement, optional emphasized subset."""
        s = scene
        emph = set(emph or [])
        fig, ax = plt.subplots(figsize=(6.4, 5))
        for i in range(s.n):
            strong = (not dim_others) or (i in emph)
            ec = (edge_colors or {}).get(
                i, "#333" if i in emph else TYPE_EDGE[s.typ[i]])
            ax.add_patch(Circle(s.pos[i], s.rad[i],
                                facecolor=TYPE_FACE[s.typ[i]], edgecolor=ec,
                                alpha=.85 if strong else .18,
                                lw=2.6 if i in emph else 1.2, zorder=2))
            ax.plot(*s.pos[i], "o", color="k", ms=3,
                    alpha=1 if strong else .25, zorder=4)
            ax.annotate(s.name[i], s.pos[i], textcoords="offset points",
                        xytext=(5, 5), fontsize=9,
                        alpha=1 if strong else .3, zorder=5)
        for i, j in itertools.combinations(range(s.n), 2):
            if s.adj[i][j]:
                both = i in emph and j in emph
                ax.plot(*np.c_[s.pos[i], s.pos[j]],
                        color="#444" if both and emph else "#999",
                        lw=2.2 if both and emph else 0.9,
                        alpha=.9 if (both or not dim_others) else .15, zorder=3)
        ax.set_title(title, fontsize=11)
        ax.set_aspect("equal"); ax.set_xlim(-4.1, 4.3); ax.set_ylim(-3.1, 3.1)
        ax.axis("off")
        fig.tight_layout()
        return fig


    def _finish(fig, save):
        if save:
            fig.savefig(save, dpi=160, bbox_inches="tight")
        return fig


    def fig_disk_graph(scene, save=None):
        """(a) D_2 — the disk graph: disks colored by radius type, gray edges."""
        return _finish(_draw(
            scene,
            r"$\mathcal{D}_2$: disk graph, $k=2$ radius types"
            "\n(blue = type-1 $(r_1)$, orange = type-2 $(r_2)$; gray = edges)"),
            save)


    def fig_single_type_clique(scene, members=(0, 1, 2), save=None):
        """(b) C_1 — a clique containing only type-1 disks."""
        return _finish(_draw(
            scene, r"$C_1$: a clique containing only type-1 disks",
            emph=list(members), dim_others=True), save)


    def fig_max_clique(scene, save=None):
        """(c) calligraphic C — the maximum clique (computed, not hand-picked)."""
        return _finish(_draw(
            scene,
            r"$\mathcal{C}$: a maximum clique of $\mathcal{D}_2$"
            r" (here $|\mathcal{C}|=%d$)" % len(scene.cmax),
            emph=scene.cmax, dim_others=True), save)


    def fig_type_classes(scene, save=None):
        """(d) calligraphic C_1, C_2 — maximal same-type cliques inside C."""
        colors = {**{i: TYPE_EDGE[1] for i in scene.c1},
                  **{i: TYPE_EDGE[2] for i in scene.c2}}
        return _finish(_draw(
            scene,
            r"$\mathcal{C}_1,\ \mathcal{C}_2$: maximal same-type cliques"
            r" inside $\mathcal{C}$",
            emph=scene.cmax, dim_others=True, edge_colors=colors), save)

    return (
        fig_disk_graph,
        fig_max_clique,
        fig_single_type_clique,
        fig_type_classes,
        make_scene,
    )


@app.cell
def _(
    fig_disk_graph,
    fig_max_clique,
    fig_single_type_clique,
    fig_type_classes,
    make_scene,
):
    scene = make_scene()
    disk_graph_fig = fig_disk_graph(scene)                  # 𝒟₂
    disk_graph_fig.savefig("figs/chapter3/notation/disk_graph_fig.png", dpi=300)

    single_type_clique_fig = fig_single_type_clique(scene)  # C₁
    single_type_clique_fig.savefig("figs/chapter3/notation/single_type_clique_fig.png", dpi=300)

    max_clique_fig = fig_max_clique(scene)                  # 𝒞
    max_clique_fig.savefig("figs/chapter3/notation/max_clique_fig.png", dpi=300)

    type_classes_fig = fig_type_classes(scene)              # 𝒞₁, 𝒞₂
    type_classes_fig.savefig("figs/chapter3/notation/type_classes_fig.png", dpi=300)
    return


if __name__ == "__main__":
    app.run()
