"""Functions for drawing edges.

In drawing edges, we need to know some pieces of information beforehand.

Firstly,
"""

from copy import deepcopy
from functools import partial, update_wrapper
from typing import Callable, Dict, Hashable

import janitor
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from datashader.bundling import hammer_bundle

from nxviz import aesthetics, lines
from nxviz.utils import edge_table

default_edge_kwargs = dict(facecolor="none", zorder=0)


# def update_default_edge_kwargs(edge_kwargs):
#     edgekw = deepcopy(default_edge_kwargs)
#     edgekw.update(edge_kwargs)
#     return edgekw


# def bundle(G, pos, ax=None, edge_kwargs={}):
#     edge_df = edge_table(G)
#     node_df = (
#         pd.DataFrame(pos)
#         .T.reset_index()
#         .rename_columns({0: "x", 1: "y", "index": "name"})
#     )
#     hb = hammer_bundle(nodes=node_df, edges=edge_df)
#     if ax is None:
#         ax = plt.gca()
#     ax = hb.plot(x="x", y="y", ax=ax)
#     ax.legend().remove()


def line_width(et: pd.DataFrame, lw_by: Hashable):
    """Default edge line width function."""
    if lw_by is not None:
        return aesthetics.data_linewidth(et[lw_by])
    return pd.Series([1] * len(et), name="lw")


def transparency(et: pd.DataFrame, alpha_by: Hashable):
    """Default edge line transparency function."""
    if alpha_by is not None:
        return aesthetics.data_transparency(et[alpha_by])
    return pd.Series([0.1] * len(et), name="alpha")


def edge_colors(et: pd.DataFrame, color_by: Hashable):
    """Default edge line color function."""
    if color_by:
        return aesthetics.data_color(et[color_by])
    return pd.Series(["black"] * len(et), name="color_by")


def draw(
    G: nx.Graph,
    pos: Dict[Hashable, np.ndarray],
    lines_func: Callable,
    color_by: Hashable = None,
    lw_by: Hashable = None,
    alpha_by: Hashable = None,
    ax=None,
    aesthetics_kwargs: Dict = {},
    **linefunc_kwargs,
):
    """Draw edges to matplotlib axes.

    ## Parameters

    - `G`: A NetworkX graph.
    - `pos`: A dictionary mapping for x,y coordinates of a node.
    - `lines_func`: One of the line drawing functions from `nxviz.lines`
    - `color_by`: Categorical or quantitative edge attribute key to color edges by.
    - `lw_by`: Quantitative edge attribute key to determine line width.
    - `alpha_by`: Quantitative edge attribute key to determine transparency.
    - `ax`: Matplotlib axes object to plot onto.
    - `aesthetics_kwargs`: A dictionary of kwargs
        to determine the aesthetic properties of the edge.
    - `linefunc_kwargs`: All other keyword arguments passed in
        will be passed onto the appropriate linefunc.

    Special keyword arguments for `aesthetics_kwargs` include:

    - `lw_scale`: A scaling factor for all edges' line widths.
        Equivalent to multiplying all line widths by this number.
    - `alpha_scale`: A scaling factor for all edges' line transparencies.
        Equivalent to multiplying all alphas by this number.
        The default transparency is 0.1,
        so an alpha_scale of any number greater than or equal to 10
        will result in 100% opaque lines.

    Everything else passed in here will be passed
    to the matplotlib Patch constructor;
    see `nxviz.lines` for more information.
    """
    et = edge_table(G)
    if ax is None:
        ax = plt.gca()
    edge_color = edge_colors(et, color_by)
    lw = line_width(et, lw_by) * aesthetics_kwargs.pop("lw_scale", 1.0)
    alpha = transparency(et, alpha_by) * aesthetics_kwargs.pop("alpha_scale", 1.0)

    aes_kw = {"zorder": 0, "facecolor": "none"}
    aes_kw.update(aesthetics_kwargs)
    patches = lines_func(
        et,
        pos,
        edge_color=edge_color,
        alpha=alpha,
        lw=lw,
        aes_kw=aes_kw,
        **linefunc_kwargs,
    )
    for patch in patches:
        ax.add_patch(patch)


circos = partial(draw, lines_func=lines.circos)
line = partial(draw, lines_func=lines.line)
arc = partial(draw, lines_func=lines.arc)
hive = partial(draw, lines_func=lines.hive)
matrix = partial(draw, lines_func=lines.matrix)

update_wrapper(circos, draw)
update_wrapper(line, draw)
update_wrapper(arc, draw)
update_wrapper(hive, draw)
update_wrapper(matrix, draw)
