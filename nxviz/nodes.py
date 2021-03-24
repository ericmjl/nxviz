from copy import deepcopy
from functools import partial
from typing import Callable, Dict, Hashable

import networkx as nx
import numpy as np
import pandas as pd

from nxviz import aesthetics
from nxviz.utils import node_table

from . import layouts


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


from matplotlib.patches import Circle


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


import matplotlib.pyplot as plt


def rescale(G):
    """Default rescale."""
    ax = plt.gca()
    ax.relim()
    ax.autoscale_view()


def rescale_arc(G):
    """Axes rescale function for arc plot."""
    ax = plt.gca()
    ax.relim()
    ymin, ymax = ax.get_ylim()
    maxheight = int(len(G) / 2) + 1
    ax.set_ylim(ymin - 1, maxheight)
    ax.set_xlim(-1, len(G) + 1)


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
    """
    node_kwargs:

    - size_scale: float - scaling factor for size.
    """
    if ax is None:
        ax = plt.gca()
    nt = node_table(G)
    pos = layout_func(nt, group_by, sort_by, **layout_kwargs)
    node_color = node_colors(nt, color_by)
    alpha = transparency(nt, alpha_by)
    size = node_size(nt, size_by) * aesthetics_kwargs.pop("size_scale", 1)
    patches = node_glyphs(nt, pos, node_color, alpha, size, **aesthetics_kwargs)
    for patch in patches:
        ax.add_patch(patch)

    rescale_func(G)
    return pos


hive = partial(draw, layout_func=layouts.hive, sort_by=None)
circos = partial(draw, layout_func=layouts.circos, group_by=None, sort_by=None)
arc = partial(
    draw,
    layout_func=layouts.arc,
    group_by=None,
    sort_by=None,
    rescale_func=rescale_arc,
)
parallel = partial(draw, layout_func=layouts.parallel, sort_by=None)
