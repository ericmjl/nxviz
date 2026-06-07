# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.8",
#     "matplotlib>=3.3.3",
#     "networkx>=2.5",
#     "numpy>=1.19.4",
#     "pandas>=1.2.0",
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
    # Low-level API

    The `nxviz` low level API is one that provides the most flexibility for constructing rational graph visualizations.

    As always, with rational graph visualizations,
    there is a process involved that helps us compose together beautiful visualizations.
    We first concern ourselves with the node placement
    using the layout functions.
    Then, we concern ourselves with data-driven visual styling of the nodes.
    After that, we figure out how to draw edges (whether as lines or bezier curves)
    and style them according to data.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Example

    As an example, let's see how we make can make customizations to the Circos plot by using the low-level API.

    For some of these things, we might be able to accomplish them using the higher level API,
    but we will intentionally show the low-level way of handling these customizations
    so that you can have a feel for how you can implement low-level customizations.
    """)
    return


@app.cell
def _():
    from random import choice

    import networkx as nx
    import numpy as np

    G = nx.erdos_renyi_graph(n=71, p=0.1)
    for n, d in G.nodes(data=True):
        G.nodes[n]["group"] = choice(["a", "b", "c"])
        G.nodes[n]["value"] = np.random.exponential()

    np.random.seed(44)
    for u, v, d in G.edges(data=True):
        G.edges[u, v]["edge_value"] = np.random.exponential()
    return G, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Node and Edge Table

    The node and edge tables are the low-level data structures that are used in creating network visualizations.
    These are pandas DataFrames.
    """)
    return


@app.cell
def _(G):
    from nxviz import utils

    nt = utils.node_table(G)
    nt.head()
    return nt, utils


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The node table is indexed by node ID, and all of the metadata attributes are stored as columns.
    """)
    return


@app.cell
def _(G, utils):
    _et = utils.edge_table(G)
    _et.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the edge table, the "source" and "target" columns are the node IDs in the node table.
    Every other column is a metadata field.
    The index carries no semantic meaning here.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Circos layout

    Following the principles of rational graph visualization,
    we start by declaring the layout that we want.
    Since in our example we'll be using the Circos plot layout,
    let's start by obtaining the (x, y) coordinate positions of each node that we want to plot.

    The `nxviz.layouts` module contains the circos plot layout function that we'll want.
    Underneath the hood, it uses pandas' group-by and sorting functionality
    to get nodes into the correct order that we want.
    If you wish to group and sort in a customized fashion,
    then you'll have to implement the functionality yourself.
    """)
    return


@app.cell
def _(nt):
    from nxviz import layouts
    _pos = layouts.circos(nt, group_by='group')
    return (layouts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Node styling

    Next, we concern ourselves with the styling of the nodes.
    Here, the `nxviz.encodings` submodule becomes useful for us.

    When drawing nodes, their color, transparency, and size can be most naturally mapped to data.

    - Transparency requires that a _quantitative_ value be mappable to the interval (0, 1).
    - Size requires that a _quantitative_ value be mappable to the positive floats (0, +inf).
    - Color is the trickiest of them all:
        - A categorical variable should be mapped to a categorical colormap.
        - A continuous variable should be mapped to a continuous colormap.

    The choice of colormap is always going to be dependent on the user.
    If you're looking for a guide on how to choose colormaps,
    the [Points of View][pov] guide to colors is a very good resource to start with.

    [pov]: http://blogs.nature.com/methagora/2013/07/data-visualization-points-of-view.html

    How do we handle styling of nodes?
    The primary way of doing so is to have a Python function
    that maps from the node table's column of values (passed in as a pandas Series)
    to any color specification that matplotlib can handle:

    - Strings: "black", "yellow", "blue", etc.
    - RGB(A): `(0.1, 0.8, 0.3, 0.5)`
    - Hexadecimal: `#FFFFFF`, `#000000`, `#A7C91F`

    Here's two examples, one using a highly custom mapping, and the other using matplotlib's color maps.
    """)
    return


@app.cell
def _(np):
    import matplotlib.pyplot as plt
    import pandas as pd


    def group_colormap(data: pd.Series):
        cmap = {"a": "black", "b": "blue", "c": "red"}
        return data.apply(lambda x: cmap.get(x))


    def value_colormap(data: pd.Series):
        """Value colormap."""
        norm = plt.cm.Normalize(vmin=data.min(), vmax=data.max())
        cmap = plt.cm.get_cmap("viridis")
        return data.apply(lambda x: cmap(norm(x)))


    def node_size(data: pd.Series):
        return data.apply(np.sqrt)

    return group_colormap, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now combine everything together, into something that basically reconstructs
    `nodes.draw`.
    """)
    return


@app.cell
def _():
    import inspect

    from nxviz import nodes, plots

    print(inspect.getsource(nodes.draw))
    return inspect, nodes, plots


@app.cell
def _(G, group_colormap, layouts, nodes, plots, plt, utils):
    _ax = plt.gca()
    nt_1 = utils.node_table(G)
    _pos = layouts.circos(nt_1, group_by='group', sort_by='value')
    _node_color = group_colormap(nt_1['group'])
    _alpha = nodes.transparency(nt_1, alpha_by=None)
    _size = nodes.node_size(nt_1, 'value')
    _patches = nodes.node_glyphs(nt_1, _pos, node_color=_node_color, alpha=_alpha, size=_size)
    for _patch in _patches:
        _ax.add_patch(_patch)
    plots.rescale(G)
    plots.aspect_equal()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Voila! We now have a sonic hedgehog-style node layout! Pretty cool, isn't it?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Adding in edges
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Once the node layout is complete, customizing the edge styling is a matter of concerning ourselves with:

    1. Line width
    2. Transparency
    3. Color

    We could customize more, but these three are the most commonly-used for mapping data to style.
    As with node layouts, we basically have to re-create `nxviz.edges.draw`
    with customized data-to-style mapping functions.
    """)
    return


@app.cell
def _(inspect):
    from nxviz import edges

    print(inspect.getsource(edges.draw))
    return (edges,)


@app.cell
def _(G, edges, group_colormap, layouts, nodes, np, plots, plt, utils):
    from nxviz import lines
    _ax = plt.gca()
    nt_2 = utils.node_table(G)
    _pos = layouts.circos(nt_2, group_by='group', sort_by='value')
    _node_color = group_colormap(nt_2['group'])
    _alpha = nodes.transparency(nt_2, alpha_by=None)
    _size = nodes.node_size(nt_2, 'value')
    _patches = nodes.node_glyphs(nt_2, _pos, node_color=_node_color, alpha=_alpha, size=_size)
    for _patch in _patches:
        _ax.add_patch(_patch)
    _et = utils.edge_table(G)
    _edge_color = edges.edge_colors(_et, nt=None, color_by=None, node_color_by=None)
    _lw = np.sqrt(_et['edge_value'])
    _alpha = edges.transparency(_et, alpha_by=None)
    _patches = lines.circos(_et, _pos, edge_color=_edge_color, alpha=_alpha, lw=_lw, aes_kw={'fc': 'none'})
    for _patch in _patches:
        _ax.add_patch(_patch)
    plots.rescale(G)
    plots.aspect_equal()
    plots.despine()
    return (lines,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Looking at the plot, we might find that expressing the edges' `edge_value` as line width might not be that effective. Instead, we might want to express it using alpha.
    """)
    return


@app.cell
def _(G, edges, group_colormap, layouts, lines, nodes, plots, plt, utils):
    _ax = plt.gca()
    nt_3 = utils.node_table(G)
    _pos = layouts.circos(nt_3, group_by='group', sort_by='value')
    _node_color = group_colormap(nt_3['group'])
    _alpha = nodes.transparency(nt_3, alpha_by=None)
    _size = nodes.node_size(nt_3, 'value')
    _patches = nodes.node_glyphs(nt_3, _pos, node_color=_node_color, alpha=_alpha, size=_size)
    for _patch in _patches:
        _ax.add_patch(_patch)
    _et = utils.edge_table(G)
    _edge_color = edges.edge_colors(_et, nt=None, color_by=None, node_color_by=None)
    _lw = edges.line_width(_et, lw_by=None)
    _alpha = edges.transparency(_et, alpha_by='edge_value')
    _patches = lines.circos(_et, _pos, edge_color=_edge_color, alpha=_alpha, lw=_lw, aes_kw={'fc': 'none'})
    for _patch in _patches:
        _ax.add_patch(_patch)
    plots.rescale(G)
    plots.aspect_equal()
    plots.despine()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Looking at this plot, it's a lot easier for us to see the important edges (as visualized by the alpha value).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusion

    Throughout this notebook, we dropped down from the mid-level API to the low-level API,
    where we get to customize node and edge styling to our heart's content.
    The patterns are easy to follow.
    For nodes, we customize the **size, color and transparency**.
    For edges we customize the **line width, color, and transparency**.
    We can then compose them together into the plots we see above.
    """)
    return


if __name__ == "__main__":
    app.run()
