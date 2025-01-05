"""Functions to encode data inside visual properties of nodes and edges."""

from functools import partial
from typing import Callable, Tuple, Optional, Union, Dict, List
from itertools import cycle

import numpy as np
import pandas as pd

from matplotlib.cm import get_cmap
from matplotlib.colors import ListedColormap, Normalize, BoundaryNorm
from palettable.colorbrewer import qualitative, sequential

from nxviz.utils import infer_data_family


def data_cmap(data: pd.Series, palette: Optional[Union[Dict, List]] = None) -> Tuple:
    """Return a colormap for data attribute.

    Returns both the cmap and data family.
    """
    data_family = infer_data_family(data)
    if data_family == "categorical":
        if palette is None:
            base_cmap = qualitative
            num_categories = max(len(data.unique()), 3)
            if num_categories > 12:
                raise ValueError(
                    f"It appears you have >12 categories for the key {data.name}. "
                    "Because it's difficult to discern >12 categories, "
                    "and because colorbrewer doesn't have a qualitative colormap "
                    "with greater than 12 categories, "
                    "nxviz does not support plotting with >12 categories. "
                    "Please provide your own palette."
                )
            cmap = ListedColormap(
                base_cmap.__dict__[f"Set3_{num_categories}"].mpl_colors
            )
        else:
            cmap = palette
    elif data_family == "ordinal":
        cmap = get_cmap("viridis")
    elif data_family == "continuous":
        cmap = get_cmap("viridis")
    elif data_family == "divergent":
        cmap = get_cmap("bwr")
    return cmap, data_family


def continuous_color_func(val, cmap, data: pd.Series):
    """Return RGBA of a value.

    ## Parameters

    - `val`: Value to convert to RGBA
    - `cmap`: A Matplotlib cmap
    - `data`: Pandas series.
    """
    norm = Normalize(vmin=data.min(), vmax=data.max())
    return cmap(norm(val))


def divergent_color_func(val, cmap, data: pd.Series):
    """Return RGBA for divergent color func.

    Divergent colormaps are best made symmetric.
    Hence, vmin and vmax are set appropriately here.
    """
    vmin = min(data.min(), -data.max())
    vmax = max(data.max(), -data.min())
    norm = Normalize(vmin=vmin, vmax=vmax)
    return cmap(norm(val))


def discrete_color_func(
    val, cmap, data: pd.Series, palette: Optional[Union[Dict, List]] = None
):
    """Return RGB corresponding to a value.

    ## Parameters

    - `val`: Value to convert to RGBA
    - `cmap`: A Matplotlib cmap
    - `data`: Pandas series.
    """
    if palette is not None:
        if isinstance(palette, dict):
            return palette[val]
        else:
            pal = dict(zip(data.unique(), cycle(palette)))
            return pal[val]
    else:
        colors = sorted(data.unique())
        return cmap.colors[colors.index(val)]


def ordinal_color_func(val, cmap, data):
    """Return RGB corresponding to an ordinal value.

    ## Parameters

    - `val`: Value to convert to RGBA
    - `cmap`: A Matplotlib cmap
    - `data`: Pandas series.
    """
    bounds = np.arange(data.min(), data.max())
    norm = BoundaryNorm(bounds, cmap.N)
    return cmap(norm(val))


def color_func(
    data: pd.Series, palette: Optional[Union[Dict, List]] = None
) -> Callable:
    """Return a color function that takes in a value and returns an RGB(A) tuple.

    This will do the mapping to the continuous and discrete color functions.
    """
    cmap, data_family = data_cmap(data, palette)
    func = discrete_color_func
    if data_family in ["continuous", "ordinal"]:
        func = continuous_color_func
        return partial(func, cmap=cmap, data=data)
    else:
        return partial(func, cmap=cmap, data=data, palette=palette)


def data_color(
    data: pd.Series, ref_data: pd.Series, palette: Optional[Union[Dict, List]] = None
) -> pd.Series:
    """Return iterable of colors for a given data.

    `cfunc` gives users the ability to customize the color mapping of a node.
    The only thing that we expect is that it takes in a value
    and returns a matplotlib-compatible RGB(A) tuple or hexadecimal value.

    The function takes in `ref_data`
    which is used to determine important colormap values (such as boundaries).
    That colormap is then applied to the actual `data`.

    ## Parameters

    - `data`: The data on which to map colors.
    - `ref_data`: The data on which the colormap is constructed.
    - `palette`: Optional custom palette of colours for plotting categorical groupings
        in a list/dictionary. Colours must be values `matplotlib.colors.ListedColormap`
        can interpret. If a dictionary is provided, key and record corresponds to
        category and colour respectively.
    """
    cfunc = color_func(ref_data, palette)
    return data.apply(cfunc)


def data_transparency(data: pd.Series, ref_data: pd.Series) -> pd.Series:
    """Transparency based on value."""
    norm = Normalize(vmin=ref_data.min(), vmax=ref_data.max())
    return data.apply(norm)


def data_size(data: pd.Series, ref_data: pd.Series) -> pd.Series:
    """Square root node size."""
    return data.apply(np.sqrt)


def data_linewidth(data: pd.Series, ref_data: pd.Series) -> pd.Series:
    """Line width scales linearly with property (by default)."""
    return data
