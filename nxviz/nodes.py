"""Node drawing functions."""

from copy import deepcopy
from functools import partial, update_wrapper
from typing import Callable, Dict, Hashable, Optional, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib.patches import Circle

from nxviz import encodings, layouts
from nxviz.utils import node_table
from nxviz.plots import rescale, rescale_arc, rescale_square


def node_colors(nt: pd.DataFrame, color_by: Hashable):
    """Return pandas Series of node colors."""
    if color_by:
        return encodings.data_color(nt[color_by], nt[color_by])
    return pd.Series(["blue"] * len(nt), name="color_by", index=nt.index)


def transparency(
    nt: pd.DataFrame, alpha_by: Hashable, alpha_bounds: Optional[Tuple] = None
):
    """Return pandas Series of transparency (alpha) values.

    Transparency must always be normalized to (0, 1)."""
    if alpha_by is not None:
        ref_data = nt[alpha_by]
        if isinstance(alpha_bounds, tuple):
            ref_data = pd.Series(alpha_bounds)

        return encodings.data_transparency(nt[alpha_by], ref_data)
    return pd.Series([1.0] * len(nt), name="transparency", index=nt.index)


def node_size(nt: pd.DataFrame, size_by: Hashable):
    """Return pandas Series of node sizes."""
    if size_by:
        return encodings.data_size(nt[size_by], nt[size_by])
    return pd.Series([1.0] * len(nt), name="size", index=nt.index)


def node_glyphs(nt, pos, node_color, alpha, size, **encodings_kwargs):
    """Draw circos glyphs to the matplotlib axes object."""
    patches = dict()
    for r, d in nt.iterrows():
        kw = {"fc": node_color[r], "alpha": alpha[r], "radius": size[r], "zorder": 2}
        kw.update(encodings_kwargs)
        c = Circle(xy=pos[r], **kw)
        patches[r] = c
    return pd.Series(patches)


def draw(
    G: nx.Graph,
    layout_func: Callable,
    group_by: Hashable,
    sort_by: Hashable,
    color_by: Hashable = None,
    alpha_by: Hashable = None,
    size_by: Hashable = None,
    layout_kwargs: Dict = {},
    encodings_kwargs: Dict = {},
    rescale_func=rescale,
    ax=None,
):
    """Draw nodes to matplotlib axes.

    ## Parameters

    - `G`: The graph to plot.
    - `layout_func`: One of the node layout functions from `nxviz.layout`.
    - `group_by`: Categorical attribute key to group nodes by.
    - `sort_by`: Quantitative or ordinal attribute key to sort nodes.
    - `color_by`: Node attribute key to color nodes by.
    - `alpha_by`: Quantitative node attribute key to set transparency.
    - `size_by`: Quantitative node attribute key to set node size.
    - `layout_kwargs`: Keyword arguments to pass
        to the appropriate layout function.
    - `encodings_kwargs`: A dictionary of kwargs
        to determine the visual properties of the node.
    - `linefunc_kwargs`: All other keyword arguments passed in
        will be passed onto the appropriate linefunc.

    Special keyword arguments for `encodings_kwargs` include:

    - `size_scale`: A scaling factor for all node radii.
        Equivalent to multiplying all node radii by this number.
    - `alpha_scale`: A scaling factor for all nodes' transparencies.
        Equivalent to multiplying all alphas by this number.
        The default transparency is 1.0.
        If you need to make the nodes transparent,
        use a value smaller than one.
    - `alpha_bounds`: The bounds for transparency.
        Should be a tuple of `(lower, upper)` numbers.
        This keyword argument lets us manually set the bounds
        that we wish to have for 0 opacity (i.e. transparent)
        to 1.0 opacity (i.e. opaque.)

    Everything else passed in here will be passed
    to the matplotlib Patch constructor;
    see `nxviz.lines` for more information.
    """
    if ax is None:
        ax = plt.gca()
    nt = node_table(G)
    pos = layout_func(nt, group_by, sort_by, **layout_kwargs)
    node_color = node_colors(nt, color_by)

    encodings_kwargs = deepcopy(encodings_kwargs)
    alpha_bounds = encodings_kwargs.pop("alpha_bounds", None)
    alpha = transparency(nt, alpha_by, alpha_bounds) * encodings_kwargs.pop(
        "alpha_scale", 1
    )
    size = node_size(nt, size_by) * encodings_kwargs.pop("size_scale", 1)
    patches = node_glyphs(nt, pos, node_color, alpha, size, **encodings_kwargs)
    for patch in patches:
        ax.add_patch(patch)

    rescale_func(G)
    return pos


hive = partial(
    draw,
    layout_func=layouts.hive,
    sort_by=None,
    layout_kwargs={"inner_radius": 8},
    encodings_kwargs={"size_scale": 0.5},
    rescale_func=rescale_square,
)
update_wrapper(hive, draw)
hive.__name__ = "nodes.hive"

circos = partial(
    draw,
    layout_func=layouts.circos,
    group_by=None,
    sort_by=None,
)
update_wrapper(circos, draw)
circos.__name__ = "nodes.circos"

arc = partial(
    draw,
    layout_func=layouts.arc,
    group_by=None,
    sort_by=None,
    rescale_func=rescale_arc,
)
update_wrapper(arc, draw)
arc.__name__ = "nodes.arc"

parallel = partial(
    draw,
    layout_func=layouts.parallel,
    sort_by=None,
    encodings_kwargs={"size_scale": 0.5},
)
update_wrapper(parallel, draw)
parallel.__name__ = "nodes.parallel"

matrix = partial(draw, layout_func=layouts.matrix, group_by=None, sort_by=None)
update_wrapper(matrix, draw)
matrix.__name__ = "nodes.matrix"

geo = partial(
    draw,
    layout_func=layouts.geo,
    group_by=None,
    sort_by=None,
    encodings_kwargs={"size_scale": 0.0015},
)
update_wrapper(geo, draw)
geo.__name__ = "nodes.geo"
