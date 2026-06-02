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
    # Implementing a new plot

    We'll show you how to implement a new plot using the nxviz's layered API.

    As an example, we'll show you how the design process works
    for the matrix plot.
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
    ## Example graph

    As always, we'll need an example graph to anchor our notebook.
    """)
    return


@app.cell
def _():
    from random import choice

    import networkx as nx
    import numpy as np

    G = nx.erdos_renyi_graph(n=20, p=0.1)
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
    ## Implement node layout

    We first have to worry about how the nodes are placed.
    Therefore, we need a node layout function.

    All node layout functions accept the following arguments:

    - a node table `nt`,
    - the key to `group_by`
    - the key to `sort_by` (optionally)
    - any other relevant keyword arguments

    With the matrix plot layout,
    from thinking about how the nodes should be laid out,
    we will probably arrive at the conclusion
    that grouping and sorting are technically optional
    and not intrinsic to the layout.
    If that's not obvious at first glance,
    please think about it, you'll probably arrive at the same conclusion!

    They then return the x, y coordinates to place nodes on.

    The exact glyphs and their styles are out-of-bounds!
    Therefore, don't worry about them just yet.
    """)
    return


@app.cell
def _():
    from typing import Hashable
    import pandas as pd
    from nxviz.utils import group_and_sort

    def matrix_layout(nt: pd.DataFrame, group_by: Hashable=None, sort_by: Hashable=None):
    # Just the skeleton first!
        _nt = group_and_sort(nt=_nt, group_by=group_by, sort_by=sort_by)

    return Hashable, group_and_sort, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With a matrix plot, our goal is to place nodes along the x- and y-axis.
    It's a bit like the hive plot with cloned axes.

    See the code annotations for the logic.
    """)
    return


@app.cell
def _(Hashable, group_and_sort, np, pd):
    def matrix_layout_1(nt: pd.DataFrame, group_by: Hashable=None, sort_by: Hashable=None, axis='x'):
        _nt = group_and_sort(node_table=_nt, group_by=group_by, sort_by=sort_by)
        pos = dict()
        for i, (node, data) in enumerate(_nt.iterrows()):
            x = (i + 1) * 2
            y = 0
            if axis == 'y':
                x, y = (y, x)
            pos[node] = np.array([x, y])
        return pos

    return (matrix_layout_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have the positions implemented, let's see what they look like.
    """)
    return


@app.cell
def _(G, matrix_layout_1):
    from nxviz.utils import node_table
    _nt = node_table(G)
    pos_x = matrix_layout_1(_nt, group_by='group', sort_by='value')
    pos_y = matrix_layout_1(_nt, group_by='group', sort_by='value', axis='y')
    return node_table, pos_x, pos_y


@app.cell
def _(pd, pos_x):
    pd.DataFrame(pos_x).T
    return


@app.cell
def _(pd, pos_y):
    pd.DataFrame(pos_y).T
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, we can worry about the glyphs being drawn to screen.
    We will follow the logic for the mid-level API.
    There is a `draw` function that we can take advantage of
    to make it happen.
    """)
    return


@app.cell
def _():
    from functools import partial

    from nxviz import nodes

    return nodes, partial


@app.cell
def _(G, matrix_layout_1, nodes, partial):
    matrix = partial(nodes.draw, layout_func=matrix_layout_1, group_by=None, sort_by=None)
    pos_x_1 = matrix(G)
    pos_y_1 = matrix(G, layout_kwargs=dict(axis='y'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Not bad! We're off to a good start.
    This looks ugly, but upon inspection, its' because the aspect ratio isn't that good.
    We can fix this.
    """)
    return


@app.cell
def _(G, matrix_layout_1, nodes, partial):
    from nxviz.plots import aspect_equal, despine
    matrix_1 = partial(nodes.draw, layout_func=matrix_layout_1, group_by=None, sort_by=None)
    pos_x_2 = matrix_1(G)
    pos_y_2 = matrix_1(G, layout_kwargs=dict(axis='y'))
    aspect_equal()
    despine()
    return aspect_equal, despine


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that's looking good! We have a square matrix, just as we expected.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Drawing edges

    For edges, we could take advantage of hive plot's lines.
    That would make the chart look interesting...
    like one of those arts and crafts tapestries we might have made when we were younger.
    """)
    return


@app.cell
def _(G, matrix_layout_1, nodes, partial):
    from nxviz import edges
    matrix_2 = partial(nodes.draw, layout_func=matrix_layout_1, group_by=None, sort_by=None)
    pos_x_3 = matrix_2(G)
    pos_y_3 = matrix_2(G, layout_kwargs=dict(axis='y'))
    edges.hive(G, pos_x_3, pos_cloned=pos_y_3, curves=False)
    return edges, matrix_2, pos_y_3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    However, the spirit of a matrix plot is to fill in an `n-by-n` matrix.
    Thus, we should actually be using a custom implementation of edges
    that draws in a circle glyph where needed.

    The matrix "lines" function will follow the API of the functions in the `nxviz.lines` file.
    Lines are in quotes because we're not technically writing out lines. :)
    """)
    return


@app.cell
def _(G, aspect_equal, despine, edges, matrix_2, partial, pos_y_3):
    from typing import Dict, Iterable
    from matplotlib.patches import Circle

    def matrix_lines(et, pos, pos_cloned, edge_color: Iterable, alpha: Iterable, lw: Iterable, aes_kw: Dict):
        patches = []
        for r, d in et.iterrows():
            start = d['source']
            end = d['target']
            x_start, y_start = pos_y_3[start]
            x_end, y_end = pos[end]
            x, y = (max(x_start, y_start), max(x_end, y_end))
            kw = {'fc': edge_color[r], 'alpha': alpha[r], 'radius': lw[r], 'zorder': 10}
            kw.update(aes_kw)
            patch = Circle(xy=(x, y), **kw)
            patches.append(patch)
        return patches
    matrix_edges = partial(edges.draw, lines_func=matrix_lines)
    import matplotlib.pyplot as plt
    _fig, _ax = plt.subplots(figsize=(4, 4))
    pos_x_4 = matrix_2(G, group_by='group', color_by='value', sort_by='value')
    pos_y_4 = matrix_2(G, group_by='group', color_by='value', sort_by='value', layout_kwargs=dict(axis='y'))
    edges.matrix(G, pos_x_4, pos_cloned=pos_y_4, alpha_by='edge_value')
    despine()
    aspect_equal()
    return matrix_edges, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Annotations

    We may wish to annotate the plot with additional information.
    For example, we might want to annotate the node values.
    This is doable using the same annotation tools available to us in nxviz.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Node color by group
    """)
    return


@app.cell
def _(G, aspect_equal, despine, matrix_2, matrix_edges, plt):
    from nxviz import annotate
    _fig, _ax = plt.subplots(figsize=(4, 4))
    pos_x_5 = matrix_2(G, group_by='group', color_by='group', sort_by='value')
    pos_y_5 = matrix_2(G, group_by='group', color_by='group', sort_by='value', layout_kwargs=dict(axis='y'))
    matrix_edges(G, pos_x_5, pos_cloned=pos_y_5, alpha_by='edge_value')
    annotate.node_colormapping(G, color_by='group')
    despine()
    aspect_equal()
    return (annotate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Node color by value
    """)
    return


@app.cell
def _(G, annotate, aspect_equal, despine, matrix_2, matrix_edges, plt):
    _fig, _ax = plt.subplots(figsize=(4, 4))
    pos_x_6 = matrix_2(G, group_by='group', color_by='value', sort_by='value')
    pos_y_6 = matrix_2(G, group_by='group', color_by='value', sort_by='value', layout_kwargs=dict(axis='y'))
    matrix_edges(G, pos_x_6, pos_cloned=pos_y_6, encodings_kwargs={'alpha_scale': 5})
    annotate.node_colormapping(G, color_by='value')
    despine()
    aspect_equal()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Annotating group identity

    The group identities can also be annotated on the chart itself.
    Here's how the `matrix_group` annotation function is implemented.
    """)
    return


@app.cell
def _(G, aspect_equal, despine, matrix_2, matrix_edges, node_table, plt):
    from nxviz.plots import respine

    def matrix_group(G, group_by, ax=None, offset=-3.0, xrotation=0, yrotation=0):
        if _ax is None:
            _ax = plt.gca()
        _nt = node_table(G)
        group_sizes = _nt.groupby(group_by).apply(lambda df: len(df))
        proportions = group_sizes / group_sizes.sum()
        midpoint = proportions / 2
        starting_positions = proportions.cumsum() - proportions
        label_positions = (starting_positions + midpoint) * len(G) * 2
        label_positions = label_positions + 1
        for label, position in label_positions.to_dict().items():
            y = offset
            x = position
            _ax.annotate(label, xy=(x, y), ha='center', va='center', rotation=0)
            x = offset
            y = position
            _ax.annotate(label, xy=(x, y), ha='center', va='center', rotation=90)
    _fig, _ax = plt.subplots(figsize=(4, 4))
    pos_x_7 = matrix_2(G, group_by='group', color_by='group', sort_by='value')
    pos_y_7 = matrix_2(G, group_by='group', color_by='group', sort_by='value', layout_kwargs=dict(axis='y'))
    matrix_edges(G, pos_x_7, pos_cloned=pos_y_7, alpha_by='edge_value')
    matrix_group(G, group_by='group')
    despine()
    aspect_equal()
    return matrix_group, respine


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Annotate matrix blocks

    We could also annotate the matrix blocks using the exact same logic.

    Matrix blocks are defined as the blocks of nodes in the same group,
    so this only applies to graphs for which the nodes can be grouped together.
    """)
    return


@app.cell
def _(
    G,
    aspect_equal,
    despine,
    matrix_2,
    matrix_edges,
    matrix_group,
    node_table,
    pd,
    plt,
    respine,
):
    _fig, _ax = plt.subplots(figsize=(4, 4))
    pos_x_8 = matrix_2(G, group_by='group', color_by='group', sort_by='value')
    pos_y_8 = matrix_2(G, group_by='group', color_by='group', sort_by='value', layout_kwargs=dict(axis='y'))
    matrix_edges(G, pos_x_8, pos_cloned=pos_y_8, alpha_by='edge_value')
    matrix_group(G, group_by='group')
    respine()
    aspect_equal()
    from matplotlib.patches import Rectangle
    from nxviz import encodings as aes
    _nt = node_table(G)
    group_by = 'group'
    color_by = 'group'

    def matrix_block(G, group_by, color_by=None, ax=None):
        group_sizes = _nt.groupby(group_by).apply(lambda df: len(df)) * 2
        starting_positions = group_sizes.cumsum() + 1 - group_sizes
        starting_positions
        colors = pd.Series(['black'] * len(group_sizes), index=group_sizes.index)
        if color_by:
            color_data = pd.Series(group_sizes.index, index=group_sizes.index)
            colors = aes.data_color(color_data, color_data)
        patches = []
        for label, position in starting_positions.to_dict().items():
            xy = (position, position)
            width = height = group_sizes[label]
            patch = Rectangle(xy, width, height, zorder=0, alpha=0.1, facecolor=colors[label])
            patches.append(patch)
        if _ax is None:
            _ax = plt.gca()
        for patch in patches:
            _ax.add_patch(patch)
    matrix_block(G, group_by=group_by, color_by=color_by)
    despine()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## High level API

    Of course, in showing you how to implement a matrix plot from scratch,
    we took the code and shoved it into our high-level API.
    Here's a few examples of how it's used.
    """)
    return


@app.cell
def _(G):
    import nxviz as nv
    _ax = nv.matrix(G)
    return (nv,)


@app.cell
def _(G, annotate, nv):
    _ax = nv.matrix(G, group_by='group', node_color_by='group', edge_alpha_by='edge_value')
    annotate.matrix_block(G, group_by='group', color_by='group')
    return


if __name__ == "__main__":
    app.run()
