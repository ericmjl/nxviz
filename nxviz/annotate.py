from nxviz.polcart import to_cartesian
from nxviz.geometry import item_theta, text_alignment
import pandas as pd
import numpy as np
from typing import Hashable
import matplotlib.pyplot as plt
from . import utils


def circos_group(G, group_by: Hashable, radius: int, ax=None, midpoint=True):
    """Text annotation of node grouping variable on a circos plot."""
    nt = utils.node_table(G)
    groups = nt.groupby(group_by).apply(lambda df: len(df)).sort_index()
    proportions = groups / groups.sum()
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


def hive_group(G, group_by, radius: int = 3, ax=None, offset=0):
    """Text annotation of hive plot groups."""
    nt = utils.node_table(G)
    groups = sorted(nt[group_by].unique())

    if ax is None:
        ax = plt.gca()

    for grp in groups:
        theta = item_theta(groups, grp) + offset
        x, y = to_cartesian(radius, theta)
        ha, va = text_alignment(x, y)
        ax.annotate(grp, xy=(x, y), ha=ha, va=va)


def arc_group(G, group_by, ax=None, midpoint=True, y_offset=0, rotation=45):
    if ax is None:
        ax = plt.gca()
    nt = utils.node_table(G)
    groups = nt.groupby(group_by).apply(lambda df: len(df)).sort_index()
    proportions = groups / groups.sum()
    starting_points = proportions.cumsum() - proportions
    if midpoint:
        starting_points += proportions / 2
    starting_points *= len(G)

    for label, starting_point in starting_points.to_dict().items():
        x = starting_point
        y = y_offset
        ha = "right"
        va = "top"
        ax.annotate(label, xy=(x, y), ha=ha, va=va, rotation=rotation)


def parallel_group(G, group_by, ax=None, y_offset=-0.3, rotation=45):
    if ax is None:
        ax = plt.gca()
    nt = utils.node_table(G)
    # groups = nt.groupby(group_by).apply(lambda df: len(df)).sort_index()
    groups = sorted(nt[group_by].unique())

    for i, label in enumerate(groups):
        x = i
        y = y_offset
        ha = "right"
        va = "top"
        ax.annotate(label, xy=(x, y), ha=ha, va=va, rotation=rotation)
    ax.relim()


from .aesthetics import data_cmap, color_func
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib import patches
from typing import Dict


def node_colormapping(
    G,
    color_by,
    legend_kwargs: Dict = {"loc": "upper right", "bbox_to_anchor": (0.0, 1.0)},
    ax=None,
):
    nt = utils.node_table(G)
    data = nt[color_by]
    colormapping(data, legend_kwargs, ax)


def edge_colormapping(
    G,
    color_by,
    legend_kwargs={"loc": "lower right", "bbox_to_anchor": (0.0, 0.0)},
    ax=None,
):
    if ax is None:
        ax = plt.gca()
    et = utils.edge_table(G)
    data = et[color_by]
    colormapping(data, legend_kwargs, ax)


def colormapping(data, legend_kwargs: Dict = {}, ax=None):
    """Annotate node color mapping.

    If the color attribute is continuous, a colorbar will be added to the matplotlib figure.
    Otherwise, a legend will be added.
    """
    cmap, data_family = data_cmap(data)
    if ax is None:
        ax = plt.gca()
    if data_family == "continuous":
        norm = Normalize(vmin=data.min(), vmax=data.max())
        scalarmap = ScalarMappable(
            cmap=cmap,
            norm=norm,
        )
        fig = plt.gcf()
        fig.colorbar(scalarmap)
    else:
        labels = data.drop_duplicates().sort_values()
        cfunc = color_func(data)
        colors = labels.apply(cfunc)
        patchlist = []
        for color, label in zip(colors, labels):
            data_key = patches.Patch(color=color, label=label)
            patchlist.append(data_key)
        kwargs = dict(
            loc="best",
            ncol=int(len(labels) / 2),
            # bbox_to_anchor=(0.5, -0.05),
        )
        kwargs.update(legend_kwargs)
        legend = plt.legend(handles=patchlist, **kwargs)
        ax.add_artist(legend)
