# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.8",
#     "matplotlib>=3.3.3",
#     "networkx>=2.5",
#     "pyprojroot",
#     "nxviz",
# ]
# [tool.uv.sources]
# nxviz = { path = "../..", editable = true }
# ///
import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Geo Plot

    In this notebook, we will see how to create geographic graph visualizations
    using the mid-level and high-level APIs.
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %config InlineBackend.figure_format = 'retina'
    # magic command not supported in marimo; please file an issue to add support
    # %load_ext autoreload
    # '%autoreload 2' command supported automatically in marimo
    return


@app.cell
def _():
    import pickle

    from pyprojroot import here

    import nxviz as nv
    from nxviz import annotate, edges, layouts, nodes, plots, utils

    return annotate, edges, here, layouts, nodes, nv, pickle, plots, utils


@app.cell
def _(here, pickle):
    with open(here() / "docs/examples/divvy.pkl", 'rb') as f:
        G = pickle.load(f)

    G_new = G.copy()
    for n1, n2, d in G.edges(data=True):
        if d["count"] < 150:
            G_new.remove_edge(n1, n2)
    return G, G_new


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mid-level API
    """)
    return


@app.cell
def _(G, G_new, annotate, edges, layouts, nodes, plots, utils):
    nt = utils.node_table(G_new)
    pos = nodes.draw(
        G_new,
        layout_func=layouts.geo,
        group_by=None,
        sort_by=None,
        color_by="dpcapacity",
        encodings_kwargs={"size_scale": 0.0015},
    )
    edges.line(G_new, pos)
    annotate.node_colormapping(G_new, color_by="dpcapacity")
    plots.rescale(G)
    plots.aspect_equal()
    plots.despine()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## High-level API
    """)
    return


@app.cell
def _(G_new, annotate, nv):
    nv.geo(G_new, node_color_by='dpcapacity')
    annotate.node_colormapping(G_new, color_by='dpcapacity')
    return


if __name__ == "__main__":
    app.run()
