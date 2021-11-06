"""Functions for drawing edges.

In drawing edges, we need to know some pieces of information beforehand.

Firstly,
"""

from copy import deepcopy
from functools import partial, update_wrapper
from typing import Callable, Dict, Hashable, Tuple, Optional

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from nxviz import encodings, lines
from nxviz.utils import node_table, edge_table

default_edge_kwargs = dict(facecolor="none", zorder=1)


def line_width(et: pd.DataFrame, lw_by: Hashable):
    """Default edge line width function."""
    if lw_by is not None:
        return encodings.data_linewidth(et[lw_by], et[lw_by])
    return pd.Series([1] * len(et), name="lw")


def transparency(
    et: pd.DataFrame, alpha_by: Hashable, alpha_bounds: Optional[Tuple] = None
) -> pd.Series:
    """Default edge line transparency function."""
    if alpha_by is not None:
        ref_data = et[alpha_by]
        if isinstance(alpha_bounds, tuple):
            ref_data = pd.Series(alpha_bounds)
        return encodings.data_transparency(et[alpha_by], ref_data)
    return pd.Series([0.1] * len(et), name="alpha")


def edge_colors(
    et: pd.DataFrame,
    nt: pd.DataFrame,
    color_by: Hashable,
    node_color_by: Hashable,
):
    """Default edge line color function."""
    if color_by in ("source_node_color", "target_node_color"):
        edge_select_by = color_by.split("_")[0]
        return encodings.data_color(
            et[edge_select_by].apply(nt[node_color_by].get),
            nt[node_color_by],
        )
    elif color_by:
        return encodings.data_color(et[color_by], et[color_by])
    return pd.Series(["black"] * len(et), name="color_by")


def validate_color_by(
    G: nx.Graph,
    color_by: Hashable,
    node_color_by: Hashable,
) -> None:
    """Validate `node_color_by` and `G` when `color_by` has a special value."""
    if color_by in ("source_node_color", "target_node_color"):
        if not isinstance(G, nx.DiGraph):
            raise ValueError(
                "Special values of `color_by`, can only be set for directed graphs."
            )
        elif not node_color_by:
            raise ValueError(
                "When setting `color_by` to special values,"
                " `node_color_by` also needs to be set."
            )


def draw(
    G: nx.Graph,
    pos: Dict[Hashable, np.ndarray],
    lines_func: Callable,
    color_by: Hashable = None,
    node_color_by: Hashable = None,
    lw_by: Hashable = None,
    alpha_by: Hashable = None,
    ax=None,
    encodings_kwargs: Dict = {},
    **linefunc_kwargs,
):
    """Draw edges to matplotlib axes.

    ## Parameters

    - `G`: A NetworkX graph.
    - `pos`: A dictionary mapping for x,y coordinates of a node.
    - `lines_func`: One of the line drawing functions from `nxviz.lines`
    - `color_by`: Categorical or quantitative edge attribute key to color edges by.
        There are two special value for this parameter
        when using directed graphs:
        "source_node_color" and "target_node_color".
        If these values are set, then `node_color_by` also needs to be set.
    - `node_color_by`: Node metadata attribute key
        that has been used to color nodes.
    - `node_color_by`: Node metadata attribute key that has been used to
        color nodes.
    - `lw_by`: Quantitative edge attribute key to determine line width.
    - `alpha_by`: Quantitative edge attribute key to determine transparency.
    - `ax`: Matplotlib axes object to plot onto.
    - `encodings_kwargs`: A dictionary of kwargs
        to determine the visual properties of the edge.
    - `linefunc_kwargs`: All other keyword arguments passed in
        will be passed onto the appropriate linefunc.

    Special keyword arguments for `encodings_kwargs` include:

    - `lw_scale`: A scaling factor for all edges' line widths.
        Equivalent to multiplying all line widths by this number.
    - `alpha_scale`: A scaling factor for all edges' line transparencies.
        Equivalent to multiplying all alphas by this number.
        The default transparency is 0.1,
        so an alpha_scale of any number greater than or equal to 10
        will result in 100% opaque lines.
    - `alpha_bounds`: The bounds for transparency.
        Should be a tuple of `(lower, upper)` numbers.
        This keyword argument lets us manually set the bounds
        that we wish to have for 0 opacity (i.e. transparent)
        to 1.0 opacity (i.e. opaque.)

    Everything else passed in here will be passed
    to the matplotlib Patch constructor;
    see `nxviz.lines` for more information.
    """
    nt = node_table(G)
    et = edge_table(G)
    if ax is None:
        ax = plt.gca()
    validate_color_by(G, color_by, node_color_by)
    edge_color = edge_colors(et, nt, color_by, node_color_by)
    encodings_kwargs = deepcopy(encodings_kwargs)
    lw = line_width(et, lw_by) * encodings_kwargs.pop("lw_scale", 1.0)

    alpha_bounds = encodings_kwargs.pop("alpha_bounds", None)
    alpha = transparency(et, alpha_by, alpha_bounds) * encodings_kwargs.pop(
        "alpha_scale", 1.0
    )

    aes_kw = {"facecolor": "none"}
    aes_kw.update(encodings_kwargs)
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
circos.__name__ = "edges.circos"

update_wrapper(line, draw)
line.__name__ = "edges.line"

update_wrapper(arc, draw)
arc.__name__ = "edges.arc"

update_wrapper(hive, draw)
hive.__name__ = "edges.hive"

update_wrapper(matrix, draw)
matrix.__name__ = "edges.matrix"
