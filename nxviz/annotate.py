from nxviz.polcart import to_cartesian
from nxviz.geometry import item_theta, text_alignment
import pandas as pd
import numpy as np
from typing import Hashable
import matplotlib.pyplot as plt

def circos_group(nt: pd.DataFrame, group_by: Hashable, radius: int, ax=None, midpoint=True):
    """Text annotation of a grouping variable on a circos plot."""
    groups = nt.groupby(group_by).apply(lambda df: len(df)).sort_index()
    proportions = (groups / groups.sum())
    starting_points = proportions.cumsum() - proportions
    if midpoint:
        starting_points += proportions / 2
    angles = starting_points * 360
    radians = angles.apply(lambda x: x / 360 * 2 * np.pi)

    if ax is None:
        ax = plt.gca()

    for label, theta in radians.to_dict().items():
        x, y = to_cartesian(radius, theta)
        ha, va = text_alignment(x, y)
        ax.annotate(label, xy=(x, y), ha=ha, va=va)


def hive_group(nt: pd.DataFrame, group_by: Hashable, inner_radius: int = 3, ax=None):
    """Text annotation of hive plot groups."""
    groups = sorted(nt[group_by].unique())

    if ax is None:
        ax = plt.gca()

    for grp in groups:
        theta = item_theta(groups, grp)
        x, y = to_cartesian(inner_radius, theta)
        ha, va = text_alignment(x, y)
        ax.annotate(grp, xy=(x, y), ha=ha, va=va)


from .colors import node_cmap, color_func
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib import patches
from typing import Dict


def colormapping(
    nt: pd.DataFrame, color_attr: Hashable, legend_kwargs: Dict = {}
):
    """Annotate color mapping.

    If the color attribute is continuous, a colorbar will be added to the matplotlib figure.
    Otherwise, a legend will be added.
    """
    cmap, data_family = node_cmap(nt, color_attr=color_attr)
    if data_family == "continuous":
        norm = Normalize(vmin=nt[color_attr].min(), vmax=nt[color_attr].max())
        scalarmap = ScalarMappable(
            cmap=cmap,
            norm=norm,
        )
        fig = plt.gcf()
        fig.colorbar(scalarmap)
    else:
        labels = nt[color_attr].drop_duplicates().sort_values()
        cfunc = color_func(nt, color_attr)
        colors = labels.apply(cfunc)
        patchlist = []
        for color, label in zip(colors, labels):
            data_key = patches.Patch(color=color, label=label)
            patchlist.append(data_key)
        ax = plt.gca()
        kwargs = dict(
            loc="best",
            ncol=int(len(labels) / 2),
            bbox_to_anchor=(0.5, -0.05),
        )
        kwargs.update(legend_kwargs)
        ax.legend(handles=patchlist, **kwargs)
