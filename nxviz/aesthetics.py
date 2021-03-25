import pandas as pd
from typing import Hashable, Tuple
from palettable.colorbrewer import sequential, qualitative
from matplotlib.colors import ListedColormap, PowerNorm
from nxviz.utils import infer_data_family


def data_cmap(data: pd.Series) -> Tuple:
    """Return a colormap for data attribute.

    Returns both the cmap and data family.
    """
    data_family = infer_data_family(data)
    if data_family == "categorical":
        base_cmap = qualitative
        num_categories = len(set(data))
        if num_categories > 12:
            raise ValueError(
                f"It appears you have >12 categories for the key {data.name}. "
                "Because it's difficult to discern >12 categories, "
                "and because colorbrewer doesn't have a qualitative colormap "
                "with greater than 12 categories, "
                "nxviz does not support plotting with >12 categories."
            )
        cmap = ListedColormap(base_cmap.__dict__[f"Set3_{num_categories}"].mpl_colors)
    elif data_family == "ordinal":
        base_cmap = sequential
        num_categories = len(set(data))
        cmap = ListedColormap(base_cmap.__dict__[f"YlGnBu_{num_categories}"].mpl_colors)
    elif data_family == "continuous":
        base_cmap = sequential
        cmap = base_cmap.__dict__["YlGnBu_9"].mpl_colormap
    return cmap, data_family


from matplotlib.colors import Normalize


def continuous_color_func(val, cmap, data: pd.Series):
    """Return RGBA of a value.

    ## Parameters

    - `val`: Value to convert to RGBA
    - `cmap`: A Matplotlib cmap
    - `df`: Node table for a graph.
    - `color_by`: The column in a node table to map to a color.
    """
    norm = Normalize(vmin=data.min(), vmax=data.max())
    return cmap(norm(val))


def discrete_color_func(val, cmap, data):
    """Return RGB corresponding to a value.

    ## Parameters

    - `val`: Value to convert to RGBA
    - `cmap`: A Matplotlib cmap
    - `nt`: Node table for a graph.
    - `color_by`: The column in a node table to map to a color.
    """
    colors = sorted(set(data))
    return cmap.colors[colors.index(val)]


from typing import Callable

from functools import partial


def color_func(data: pd.Series) -> Callable:
    """Return a color function that takes in a value and returns an RGB(A) tuple.

    This will do the mapping to the continuous and discrete color functions.
    """
    cmap, data_family = data_cmap(data)
    func = discrete_color_func
    if data_family == "continuous":
        func = continuous_color_func
    return partial(func, cmap=cmap, data=data)


def data_color(data: pd.Series) -> pd.Series:
    """Return iterable of colors for a given data.

    `cfunc` gives users the ability to customize the color mapping of a node.
    The only thing that we expect is that it takes in a value
    and returns a matplotlib-compatible RGB(A) tuple or hexadecimal value.
    """

    cfunc = color_func(data)
    return data.apply(cfunc)


def data_transparency(data: pd.Series) -> pd.Series:
    """Transparency based on value."""
    norm = Normalize(vmin=data.min(), vmax=data.max())
    return data.apply(norm)


def data_size(data: pd.Series) -> pd.Series:
    """Square root node size."""
    norm = PowerNorm(gamma=0.5)
    return data.apply(norm)


def data_linewidth(data: pd.Series) -> pd.Series:
    """Line width scales linearly with property (by default)."""
    return data