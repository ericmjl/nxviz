# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.8",
#     "matplotlib>=3.3.3",
#     "networkx>=2.5",
#     "numpy>=1.19.4",
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
    # Object-Oriented API

    For those who may prefer the object-oriented API of the past, we provide the following class definitions that map directly to the functions.
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
    from random import choice

    import networkx as nx
    import numpy as np

    import nxviz as nv
    from nxviz import annotate

    return annotate, choice, np, nv, nx


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Example Graph

    We're going to use an example graph, the erdos-renyi graph,
    to illustrate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Source code
    """)
    return


@app.cell
def _(choice, np, nx):
    G = nx.erdos_renyi_graph(n=71, p=0.1)
    for n, d in G.nodes(data=True):
        G.nodes[n]["group"] = choice(["a", "b", "c"])
        G.nodes[n]["value"] = np.random.exponential()

    np.random.seed(44)
    for u, v, d in G.edges(data=True):
        G.edges[u, v]["edge_value"] = np.random.exponential()
    return (G,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## API Examples

    The API from pre-0.7 is mostly preserved as a way
    to help users who learned the object-oriented API transition over.
    A key difference here is that instantiating the object
    and then calling `.draw()` is no longer necessary.
    Additionally, annotation logic has been moved out of the class definitions
    and are now available as part of the annotations submodule.

    Because the API is no longer being officially supported,
    these will be officially deprecated in version 1.0.
    A warning message will show up the first time you try to access any of the objects provided.
    PRs that try to add an object version of a plot will also be rejected.
    """)
    return


@app.cell
def _(G, annotate, np, nv):
    nv.HivePlot(G, node_grouping="group", node_color="value", node_order="value", edge_alpha="edge_value")

    annotate.hive_group(G, group_by="group", offset=np.pi / 12)
    return


@app.cell
def _(G, nv):
    nv.CircosPlot(G, node_grouping="group", node_color="value", node_order="value")
    return


@app.cell
def _(G, nv):
    nv.MatrixPlot(G, node_grouping="group", node_color="value", node_order="value")
    return


@app.cell
def _(G, annotate, nv):
    nv.ArcPlot(
        G,
        node_grouping="group",
        node_color="value",
        node_order="value",
        edge_color="edge_value",
    )
    annotate.arc_group(G, group_by="group", rotation=0)
    return


if __name__ == "__main__":
    app.run()
