from copy import deepcopy
from functools import partial, update_wrapper
from typing import Callable, Dict, Hashable

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib.patches import Circle

from nxviz import aesthetics, layouts
from nxviz.utils import node_table
from nxviz.plots import rescale, rescale_arc


def node_colors(nt: pd.DataFrame, color_by: Hashable):
    if color_by:
        return aesthetics.data_color(nt[color_by])
    return pd.Series(["blue"] * len(nt), name="color_by", index=nt.index)


def transparency(nt: pd.DataFrame, alpha_by: Hashable):
    """Transparency must always be normalized to (0, 1)."""
    if alpha_by:
        return aesthetics.data_transparency(nt[alpha_by])
    return pd.Series([1.0] * len(nt), name="transparency", index=nt.index)


def node_size(nt: pd.DataFrame, size_by: Hashable):
    if size_by:
        return aesthetics.data_size(nt[size_by])
    return pd.Series([1.0] * len(nt), name="size", index=nt.index)


def node_glyphs(nt, pos, node_color, alpha, size, **aesthetics_kwargs):
    """Draw circos glyphs to the matplotlib axes object."""
    patches = dict()
    for r, d in nt.iterrows():
        kw = {
            "fc": node_color[r],
            "alpha": alpha[r],
            "radius": size[r],
        }
        kw.update(aesthetics_kwargs)
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
    aesthetics_kwargs: Dict = {},
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
    - `aesthetics_kwargs`: A dictionary of kwargs
        to determine the aesthetic properties of the node.
    - `linefunc_kwargs`: All other keyword arguments passed in
        will be passed onto the appropriate linefunc.

    Special keyword arguments for `aesthetics_kwargs` include:

    - `size_scale`: A scaling factor for all node radii.
        Equivalent to multiplying all node radii by this number.
    - `alpha_scale`: A scaling factor for all nodes' transparencies.
        Equivalent to multiplying all alphas by this number.
        The default transparency is 1.0.
        If you need to make the nodes transparent,
        use a value smaller than one.

    Everything else passed in here will be passed
    to the matplotlib Patch constructor;
    see `nxviz.lines` for more information.
    """
    if ax is None:
        ax = plt.gca()
    nt = node_table(G)
    pos = layout_func(nt, group_by, sort_by, **layout_kwargs)
    node_color = node_colors(nt, color_by)

    aesthetics_kwargs = deepcopy(aesthetics_kwargs)
    alpha = transparency(nt, alpha_by) * aesthetics_kwargs.pop("alpha_scale", 1)
    size = node_size(nt, size_by) * aesthetics_kwargs.pop("size_scale", 1)
    patches = node_glyphs(nt, pos, node_color, alpha, size, **aesthetics_kwargs)
    for patch in patches:
        ax.add_patch(patch)

    rescale_func(G)
    return pos


hive = partial(
    draw,
    layout_func=layouts.hive,
    sort_by=None,
    layout_kwargs={"inner_radius": 8},
    aesthetics_kwargs={"size_scale": 0.5},
)
circos = partial(
    draw,
    layout_func=layouts.circos,
    group_by=None,
    sort_by=None,
    aesthetics_kwargs={"size_scale": 0.1},
)
arc = partial(
    draw,
    layout_func=layouts.arc,
    group_by=None,
    sort_by=None,
    rescale_func=rescale_arc,
)
parallel = partial(
    draw,
    layout_func=layouts.parallel,
    sort_by=None,
    aesthetics_kwargs={"size_scale": 0.5},
)

update_wrapper(circos, draw)
update_wrapper(parallel, draw)
update_wrapper(arc, draw)
update_wrapper(hive, draw)