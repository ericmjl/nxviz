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
    # Panels and Faceting

    In this notebook, we will introduce how to make graph visualization panels!
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

    import matplotlib.pyplot as plt
    import networkx as nx
    import numpy as np

    import nxviz as nv

    return choice, np, nv, nx, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Example graph

    Here's an example graph. It has both quantiative and qualitative data encoded on the nodes and edges.
    """)
    return


@app.cell
def _(choice, np, nx):
    categories = "abcdefghijk"
    node_categories = "12345"

    G = nx.erdos_renyi_graph(n=70, p=0.1)
    for u, v in G.edges():
        G.edges[u, v]["group"] = choice(categories)
        G.edges[u, v]["edge_val"] = np.random.exponential()

    for n in G.nodes():
        G.nodes[n]["category"] = choice(node_categories)
        G.nodes[n]["value"] = np.random.normal()
    return (G,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Non-panel'd version

    Let's see what happens if we just try to plot all nodes and all edges together.
    """)
    return


@app.cell
def _(G, nv):
    nv.circos(
        G,
        group_by="category",
        node_color_by="category",
        edge_color_by="edge_val",
        edge_enc_kwargs={"alpha_scale": 5},
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This isn't particularly useful.
    The edges are over-populated on the visualization.
    If there were structure in the graph that were interesting,
    we'd find it hard to elucidate.
    Here, we can rely on the principle of small multiples
    to design a more effective visualizations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `nxviz` faceting API

    Graph visualization panels are the solution here.
    We use categorical metadata on nodes or edges
    to facet our visualizations.
    (Faceting refers to creating subplots that contain a subset of the full dataset,
    so that one can optimize for visual clarity.)

    Because nodes are more easily arranged than edges,
    we can facet our graph out by edge categories into **panels**.
    As such, one subcategory of graph visualization panels
    is defined by a faceting of our graph by edge categories.
    Here are some examples.
    """)
    return


@app.cell
def _():
    from nxviz import annotate, facet

    # from nxviz import hive_panel, arc_panel, circos_panel
    return annotate, facet


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Arc Panel
    """)
    return


@app.cell
def _(G, facet):
    facet.arc_panel(
        G,
        edge_group_by="group",
        node_group_by="category",
        node_color_by="category",
        edge_color_by="edge_val",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Circos Panel
    """)
    return


@app.cell
def _(G, facet):
    facet.circos_panel(
        G,
        edge_group_by="group",
        node_group_by="category",
        node_color_by="category",
        edge_color_by="edge_val",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Matrix Panel
    """)
    return


@app.cell
def _(G, facet):
    facet.matrix_panel(
        G,
        edge_group_by="group",
        node_group_by="category",
        node_color_by="category",
        edge_color_by="edge_val",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Hive Panel

    Hive panels are a special type of panel.
    Because hive plots alone can plot either 2 or 3 categories of nodes,
    it can't handle situations where there are more than 3 categories of nodes.
    Here is where a panel of hive plots comes in:
    each plot in the panel handles 3 of the categories that are present.
    As such, you will have ${K}\choose{3}$ plots to plot.
    For this reason, we don't recommend having more than 6 categories,
    otherwise you'll end up with a lot of plots to look at.
    """)
    return


@app.cell
def _(G, facet):
    facet.hive_panel(G, node_group_by="category", node_color_by="category")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Custom panels

    While there are plot-specific faceting APIs,
    you can use the building blocks in there to compose your own.

    In this example,
    we'll show you how to create a facet where we show
    only edges that are associated with a particular group of nodes.
    For this, the key function to use is `node_group_edges`,
    which yields graphs that contains edges attached to a particular group,
    as well as the group itself.
    """)
    return


@app.cell
def _():
    import inspect

    from nxviz.facet import n_rows_cols, node_group_edges

    print(inspect.getsource(node_group_edges))
    return inspect, n_rows_cols, node_group_edges


@app.cell
def _(G, annotate, n_rows_cols, node_group_edges, nv, plt):
    node_group_by = "category"

    graphs, groups = zip(*node_group_edges(G, node_group_by))
    nrows, ncols = n_rows_cols(groups)
    fig, axes = plt.subplots(figsize=(8, 8), nrows=3, ncols=3)
    axes = list(axes.flatten())

    for ax, G_sub, group in zip(axes, graphs, groups):
        plt.sca(ax)
        nv.circos(
            G_sub, group_by="category", sort_by="value", node_color_by="category"
        )
        annotate.circos_group(G_sub, group_by="category")
        ax.set_title(f"node group = {group}")


    i = axes.index(ax)
    for ax in axes[i + 1 :]:
        fig.delaxes(ax)

    plt.tight_layout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Development pattern

    The core of faceting in nxviz is to return an iterator of graphs
    that contain either

    1. a subset of nodes,
    2. a subset of edges,
    3. or a subset of nodes and edges.

    Using one of the faceting functions as an example to illustrate:
    """)
    return


@app.cell
def _(facet, inspect):
    print(inspect.getsource(facet.edge_group))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The pattern is essentially to identify the exact groups that exist,
    iterate over these groups,
    and yield a graph that contains any one of the aforementioned three subsets
    alongside the group.
    That function pattern makes faceting consistent.
    """)
    return


if __name__ == "__main__":
    app.run()
