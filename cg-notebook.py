import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Polygon, Circle
    import math
    import marimo as mo

    return Circle, Polygon, math, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Chapter 2 Figures
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lens Geometry
    """)
    return


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
        return fig

    return (lens_geometry,)


@app.cell
def _(lens_geometry):
    lens_geometry_fig = lens_geometry()
    lens_geometry_fig.savefig('figs/chapter2/perliminaries/lens_geometry.png', dpi=300)
    lens_geometry_fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Slab Geometry
    """)
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
        return fig


    return (slab_geom,)


@app.cell
def _(slab_geom):
    slab_geom_fig = slab_geom()
    slab_geom_fig.savefig('figs/chapter2//perliminaries/slab_geometry.png', dpi=300)
    slab_geom_fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lemma 2.1
    """)
    return


@app.cell
def _(np):
    import lemma21_sliding_animation as l2anim

    def figs_lemma21():
        """---------- the two scenarios of Figure 1(b)-(c) ----------"""
        a, b = np.array([0.0, 0.0]), np.array([4.0, 0.8])

        # Case (b): p high above the slab; the ray p->q exits through segment ab itself
        s1_b = l2anim.animate_case(p=np.array([1.1, 3.4]), q=np.array([2.1, 1.2]),
                     a=a, b=b, case="b", fname="figs/chapter2/lemma21/lemma21_case_b.gif")

        # Case (c): p outside the slab to the right; the ray exits through the LEFT wall
        s1_c = l2anim.animate_case(p=np.array([5.3, 2.4]), q=np.array([3.2, 2.0]),
                     a=a, b=b, case="c", fname="figs/chapter2/lemma21/lemma21_case_c.gif")

        # Scenario 2 (degenerate): a and b share the same x-coordinate; the slab
        # collapses to the vertical line through them, and q sits on that line.
        av, bv = np.array([2.0, 0.0]), np.array([2.0, 1.6])
        s2 = l2anim.animate_case(p=np.array([3.7, 3.0]), q=np.array([2.0, 2.35]),
                     a=av, b=bv, case="v", fname="figs/chapter2/lemma21/lemma21_case_vertical.gif")
        return s1_b, s1_c, s2

    return (figs_lemma21,)


@app.cell
def _(figs_lemma21, mo):
    mo.hstack([mo.image(src=gif) for gif in figs_lemma21()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Chapter 3 Figures
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Notation Visualizations
    """)
    return


@app.cell
def _():
    import scene_figures as sf

    scene = sf.make_scene()        # 8-disk D_2 arrangement — the notation figures
    ascene = sf.make_algo_scene()  # 11-disk walk-through — Psi, slabs, X/Y filter
    return ascene, scene, sf


@app.cell
def _(scene, sf):
    disk_graph_fig = sf.fig_disk_graph(scene)                  # 𝒟₂
    disk_graph_fig.savefig("figs/chapter3/notation/disk_graph_fig.png", dpi=300)

    single_type_clique_fig = sf.fig_single_type_clique(scene)  # C₁
    single_type_clique_fig.savefig("figs/chapter3/notation/single_type_clique_fig.png", dpi=300)

    max_clique_fig = sf.fig_max_clique(scene)                  # 𝒞
    max_clique_fig.savefig("figs/chapter3/notation/max_clique_fig.png", dpi=300)

    type_classes_fig = sf.fig_type_classes(scene)              # 𝒞₁, 𝒞₂
    type_classes_fig.savefig("figs/chapter3/notation/type_classes_fig.png", dpi=300)
    return (
        disk_graph_fig,
        max_clique_fig,
        single_type_clique_fig,
        type_classes_fig,
    )


@app.cell
def _(
    disk_graph_fig,
    max_clique_fig,
    single_type_clique_fig,
    type_classes_fig,
):
    disk_graph_fig, single_type_clique_fig, max_clique_fig, type_classes_fig 
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Algorithm Walk-through (S5–S7)
    """)
    return


@app.cell
def _(ascene, sf):
    guess_fig = sf.fig_guess(ascene, save="figs/chapter3/algorithm/guess.png")
    slabs_fig = sf.fig_slabs(ascene, save="figs/chapter3/algorithm/slabs.png")
    filter_fig = sf.fig_filter(ascene, save="figs/chapter3/algorithm/filter.png")
    invalid_guess_fig = sf.fig_invalid_guess(
        ascene.s, pair=(0, 4),      # s1 and s5 — they don't intersect, so Psi isn't a clique
        save="figs/chapter3/algorithm/invalid_guess.png",
    )

    guess_fig, invalid_guess_fig, slabs_fig, filter_fig
    return


if __name__ == "__main__":
    app.run()
