import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np

    return mo, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Chapter 2 Figures
    """)
    return


@app.cell
def _():
    from chapter2_figures import lens_geometry, slab_geom

    return lens_geometry, slab_geom


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lens Geometry
    """)
    return


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


@app.cell
def _(mo):
    mo.md(r"""
    ## Assembly (S8–S11)
    """)
    return


@app.cell
def _(ascene, sf):
    x_clique_fig = sf.fig_x_clique(ascene, save="figs/chapter3/algorithm/x_clique.png")
    missing_edges_fig = sf.fig_missing_edges(ascene, save="figs/chapter3/algorithm/missing_edges.png")
    complement_fig = sf.fig_complement(ascene, save="figs/chapter3/algorithm/complement.png")
    assembly_fig = sf.fig_assembly(ascene, save="figs/chapter3/algorithm/assembly.png")

    x_clique_fig, missing_edges_fig, complement_fig, assembly_fig
    return


if __name__ == "__main__":
    app.run()
