import pandas as pd
from typing import Hashable, Tuple
from palettable.colorbrewer import sequential, qualitative
from matplotlib.colors import ListedColormap
from nxviz.utils import infer_data_family


def node_cmap(nt: pd.DataFrame, color_attr: Hashable) -> Tuple:
    """Return a colormap for node attributes.

    Returns both the cmap and data family.
    """
    data_family = infer_data_family(nt[color_attr])
    if data_family == "categorical":
        base_cmap = qualitative
        num_categories = len(set(nt[color_attr]))
        cmap = ListedColormap(base_cmap.__dict__[f"Accent_{num_categories}"].mpl_colors)
    elif data_family == "ordinal":
        base_cmap = sequential
        num_categories = len(set(nt[color_attr]))
        ListedColormap(base_cmap.Dark2_7.mpl_colors)
        cmap = ListedColormap(base_cmap.__dict__[f"YlGnBu_{num_categories}"].mpl_colors)
    elif data_family == "continuous":
        base_cmap = sequential
        cmap = base_cmap.__dict__["YlGnBu_9"].mpl_colormap
    return cmap, data_family


from matplotlib.colors import Normalize


def continuous_color_func(val, cmap, nt: pd.DataFrame, color_attr: Hashable):
    """Return RGBA of a value.

    ## Parameters

    - `val`: Value to convert to RGBA
    - `cmap`: A Matplotlib cmap
    - `nt`: Node table for a graph.
    - `color_attr`: The column in a node table to map to a color.
    """
    norm = Normalize(vmin=nt[color_attr].min(), vmax=nt[color_attr].max())
    return cmap(norm(val))


def discrete_color_func(val, cmap, nt: pd.DataFrame, color_attr: Hashable):
    """Return RGB corresponding to a value.

    ## Parameters

    - `val`: Value to convert to RGBA
    - `cmap`: A Matplotlib cmap
    - `nt`: Node table for a graph.
    - `color_attr`: The column in a node table to map to a color.
    """
    colors = sorted(set(nt[color_attr]))
    return cmap.colors[colors.index(val)]


from typing import Callable

from functools import partial


def color_func(nt, color_attr) -> Callable:
    """Return a color function that takes in a value and returns an RGB(A) tuple.

    This will do the mapping to the continuous and discrete color functions.
    """
    cmap, data_family = node_cmap(nt, color_attr=color_attr)
    func = discrete_color_func
    if data_family == "continuous":
        func = continuous_color_func
    return partial(func, cmap=cmap, nt=nt, color_attr=color_attr)


def node_colors(nt: pd.DataFrame, color_attr: Hashable, cfunc: Callable = None):
    """Return iterable of node colors for a graph's node table.

    `cfunc` gives users the ability to customize the color mapping of a node.
    The only thing that we expect is that it takes in a value
    and returns a matplotlib-compatible RGB(A) tuple or hexadecimal value.
    """

    if cfunc is None:
        cfunc = color_func(nt, color_attr)

    colors = nt[color_attr].apply(cfunc)
    return colors


from typing import Dict
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.cm import ScalarMappable
