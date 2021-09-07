"""Annotation submodule."""
from functools import partial, update_wrapper
from typing import Dict, Hashable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.patches import Patch, Rectangle

from nxviz import encodings, layouts, utils
from nxviz.geometry import circos_radius, item_theta
from nxviz.polcart import to_cartesian


def text_alignment(x, y):
    """
    Align text labels based on the x- and y-axis coordinate values.

    This function is used for computing the appropriate alignment of the text
    label.

    For example, if the text is on the "right" side of the plot, we want it to
    be left-aligned. If the text is on the "top" side of the plot, we want it
    to be bottom-aligned.

    :param x, y: (`int` or `float`) x- and y-axis coordinate respectively.
    :returns: A 2-tuple of strings, the horizontal and vertical alignments
        respectively.
    """
    if x == 0:
        ha = "center"
    elif x > 0:
        ha = "left"
    else:
        ha = "right"
    if y == 0:
        va = "center"
    elif y > 0:
        va = "bottom"
    else:
        va = "top"

    return ha, va


def circos_group(
    G,
    group_by: Hashable,
    radius: float = None,
    radius_offset: float = 1,
    ax=None,
    midpoint=True,
):
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

    if radius is None:
        radius = circos_radius(len(G)) + radius_offset

    for label, theta in radians.to_dict().items():
        x, y = to_cartesian(radius, theta)
        ha, va = text_alignment(x, y)
        ax.annotate(label, xy=(x, y), ha=ha, va=va)


def hive_group(G, group_by, ax=None, offset=np.pi / 12):
    """Text annotation of hive plot groups."""
    nt = utils.node_table(G)
    groups = sorted(nt[group_by].unique())

    if ax is None:
        ax = plt.gca()

    for grp in groups:
        theta = item_theta(groups, grp) + offset
        radius = 2 * (8 + len(nt[nt[group_by] == grp]) + 1)
        x, y = to_cartesian(radius, theta)
        ha, va = text_alignment(x, y)
        ax.annotate(grp, xy=(x, y), ha=ha, va=va)


def arc_group(
    G, group_by, ax=None, midpoint=True, y_offset=-1, rotation=45, ha="right", va="top"
):
    """Annotate arc group."""
    if ax is None:
        ax = plt.gca()
    nt = utils.node_table(G)
    groups = nt.groupby(group_by).apply(lambda df: len(df)).sort_index()
    proportions = groups / groups.sum()
    starting_points = proportions.cumsum() - proportions
    if midpoint:
        starting_points += proportions / 2
    starting_points *= len(G) * 2

    for label, starting_point in starting_points.to_dict().items():
        x = starting_point
        y = y_offset
        ax.annotate(label, xy=(x, y), ha=ha, va=va, rotation=rotation)


def parallel_group(
    G, group_by, ax=None, y_offset=-0.3, rotation=45, ha="right", va="top"
):
    """Annotate parallel plot groups."""
    if ax is None:
        ax = plt.gca()
    nt = utils.node_table(G)
    # groups = nt.groupby(group_by).apply(lambda df: len(df)).sort_index()
    groups = sorted(nt[group_by].unique())

    for i, label in enumerate(groups):
        x = i * 4
        y = y_offset
        ax.annotate(label, xy=(x, y), ha=ha, va=va, rotation=rotation)
    ax.relim()


def matrix_group(G, group_by, ax=None, offset=-3.0, xrotation=0, yrotation=90):
    """Annotate matrix plot groups."""
    if ax is None:
        ax = plt.gca()
    nt = utils.node_table(G)
    group_sizes = nt.groupby(group_by).apply(lambda df: len(df))
    proportions = group_sizes / group_sizes.sum()
    midpoint = proportions / 2
    starting_positions = proportions.cumsum() - proportions
    label_positions = (starting_positions + midpoint) * len(G) * 2
    label_positions += 1

    for label, position in label_positions.to_dict().items():
        # Plot the x-axis labels
        y = offset
        x = position
        ax.annotate(label, xy=(x, y), ha="center", va="center", rotation=xrotation)

        # Plot the y-axis labels
        x = offset
        y = position
        ax.annotate(label, xy=(x, y), ha="center", va="center", rotation=yrotation)


def matrix_block(G, group_by, color_by=None, ax=None, alpha=0.1):
    """Annotate group blocks on a matrix plot.

    Most useful for highlighting the within- vs between-group edges.
    """
    nt = utils.node_table(G)
    group_sizes = nt.groupby(group_by).apply(lambda df: len(df)) * 2
    starting_positions = group_sizes.cumsum() + 1 - group_sizes
    starting_positions

    colors = pd.Series(["black"] * len(group_sizes), index=group_sizes.index)
    if color_by:
        color_data = pd.Series(group_sizes.index, index=group_sizes.index)
        colors = encodings.data_color(color_data, color_data)
    # Generate patches first
    patches = []
    for label, position in starting_positions.to_dict().items():
        xy = (position, position)
        width = height = group_sizes[label]

        patch = Rectangle(
            xy, width, height, zorder=20, alpha=alpha, facecolor=colors[label]
        )
        patches.append(patch)

    if ax is None:
        ax = plt.gca()
    # Then add patches in.
    for patch in patches:
        ax.add_patch(patch)


def colormapping(data, legend_kwargs: Dict = {}, ax=None):
    """Annotate node color mapping.

    If the color attribute is continuous, a colorbar will be added to the matplotlib figure.
    Otherwise, a legend will be added.
    """
    cmap, data_family = encodings.data_cmap(data)
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
        cfunc = encodings.color_func(data)
        colors = labels.apply(cfunc)
        patchlist = []
        for color, label in zip(colors, labels):
            data_key = Patch(color=color, label=label)
            patchlist.append(data_key)
        kwargs = dict(
            loc="best",
            ncol=int(len(labels) / 2),
            # bbox_to_anchor=(0.5, -0.05),
        )
        kwargs.update(legend_kwargs)
        legend = plt.legend(handles=patchlist, **kwargs)
        ax.add_artist(legend)


def node_colormapping(
    G,
    color_by,
    legend_kwargs: Dict = {"loc": "upper right", "bbox_to_anchor": (0.0, 1.0)},
    ax=None,
):
    """Annotate node color mapping."""
    nt = utils.node_table(G)
    data = nt[color_by]
    colormapping(data, legend_kwargs, ax)


def edge_colormapping(
    G,
    color_by,
    legend_kwargs={"loc": "lower right", "bbox_to_anchor": (0.0, 0.0)},
    ax=None,
):
    """Annotate edge color mapping."""
    if ax is None:
        ax = plt.gca()
    et = utils.edge_table(G)
    data = et[color_by]
    colormapping(data, legend_kwargs, ax)


def node_labels(G, layout_func, group_by, sort_by, ax=None):
    """Annotate node labels."""
    if ax is None:
        ax = plt.gca()

    nt = utils.node_table(G)
    pos = layout_func(nt, group_by, sort_by)
    for node in G.nodes():
        ax.annotate(text=node, xy=pos[node], ha="center", va="center")


parallel_labels = partial(node_labels, layout_func=layouts.parallel, sort_by=None)
update_wrapper(parallel_labels, node_labels)
parallel_labels.__name__ = "annotate.parallel_labels"

hive_labels = partial(node_labels, layout_func=layouts.hive, sort_by=None)
update_wrapper(hive_labels, node_labels)
hive_labels.__name__ = "annotate.hive_labels"

arc_labels = partial(node_labels, layout_func=layouts.arc, group_by=None, sort_by=None)
update_wrapper(arc_labels, node_labels)
arc_labels.__name__ = "annotate.arc_labels"


matrix_labels = partial(
    node_labels, layout_func=layouts.matrix, group_by=None, sort_by=None
)
update_wrapper(matrix_labels, node_labels)
matrix_labels.__name__ = "annotate.matrix_labels"


circos_labels = partial(
    node_labels, layout_func=layouts.circos, group_by=None, sort_by=None
)
update_wrapper(circos_labels, node_labels)
circos_labels.__name__ = "annotate.circos_labels"
