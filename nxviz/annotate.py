"""Annotation submodule."""
from functools import partial, update_wrapper
from typing import Dict, Hashable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.patches import Patch, Rectangle

from nxviz import encodings, layouts, utils
from nxviz.geometry import circos_radius, item_theta
from nxviz.polcart import to_cartesian, to_degrees


def text_alignment(x: float, y: float):
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


def validate_fontdict(fontdict: Dict):
    """Validate `fontdict` keys."""
    valid_keys = {"family", "size", "stretch", "style", "variant", "weight"}
    assert set(fontdict) <= valid_keys


def circos_group(
    G: nx.Graph,
    group_by: Hashable,
    radius: float = None,
    radius_offset: float = 1,
    midpoint: bool = True,
    fontdict: Dict = {},
    ax=None,
):
    """Text annotation of node grouping variable on a circos plot."""
    validate_fontdict(fontdict)
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
        ax.annotate(label, xy=(x, y), ha=ha, va=va, **fontdict)


def hive_group(
    G: nx.Graph,
    group_by: Hashable,
    offset: float = np.pi / 12,
    fontdict: Dict = {},
    ax=None,
):
    """Text annotation of hive plot groups."""
    validate_fontdict(fontdict)
    nt = utils.node_table(G)
    groups = sorted(nt[group_by].unique())

    if ax is None:
        ax = plt.gca()

    for grp in groups:
        theta = item_theta(groups, grp) + offset
        radius = 2 * (8 + len(nt[nt[group_by] == grp]) + 1)
        x, y = to_cartesian(radius, theta)
        ha, va = text_alignment(x, y)
        ax.annotate(grp, xy=(x, y), ha=ha, va=va, **fontdict)


def arc_group(
    G: nx.Graph,
    group_by: Hashable,
    midpoint: bool = True,
    y_offset: float = -1,
    rotation: float = 45,
    ha: str = "right",
    va: str = "top",
    fontdict: Dict = {},
    ax=None,
):
    """Annotate arc group."""
    validate_fontdict(fontdict)
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
        ax.annotate(label, xy=(x, y), ha=ha, va=va, rotation=rotation, **fontdict)


def parallel_group(
    G: nx.Graph,
    group_by: Hashable,
    y_offset: float = -0.3,
    rotation: float = 45,
    ha: str = "right",
    va: str = "top",
    fontdict: Dict = {},
    ax=None,
):
    """Annotate parallel plot groups."""
    validate_fontdict(fontdict)
    if ax is None:
        ax = plt.gca()
    nt = utils.node_table(G)
    # groups = nt.groupby(group_by).apply(lambda df: len(df)).sort_index()
    groups = sorted(nt[group_by].unique())

    for i, label in enumerate(groups):
        x = i * 4
        y = y_offset
        ax.annotate(label, xy=(x, y), ha=ha, va=va, rotation=rotation, **fontdict)
    ax.relim()


def matrix_group(
    G: nx.Graph,
    group_by: Hashable,
    offset: float = -3,
    xrotation: float = 0,
    yrotation: float = 90,
    fontdict: Dict = {},
    ax=None,
):
    """Annotate matrix plot groups."""
    validate_fontdict(fontdict)
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
        ax.annotate(
            label,
            xy=(x, y),
            ha="center",
            va="center",
            rotation=xrotation,
            **fontdict,
        )

        # Plot the y-axis labels
        x = offset
        y = position
        ax.annotate(
            label, xy=(x, y), ha="center", va="center", rotation=yrotation, **fontdict
        )


def matrix_block(
    G: nx.Graph,
    group_by: Hashable,
    color_by: Hashable = None,
    alpha: float = 0.1,
    ax=None,
):
    """Annotate group blocks on a matrix plot.

    Most useful for highlighting the within- vs between-group edges.
    """
    nt = utils.node_table(G)
    group_sizes = nt.groupby(group_by).apply(lambda df: len(df)) * 2
    starting_positions = group_sizes.cumsum() + 1 - group_sizes

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


def colormapping(data: pd.Series, legend_kwargs: Dict = {}, ax=None):
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
    G: nx.Graph,
    color_by: Hashable,
    legend_kwargs: Dict = {"loc": "upper right", "bbox_to_anchor": (0.0, 1.0)},
    ax=None,
):
    """Annotate node color mapping."""
    nt = utils.node_table(G)
    data = nt[color_by]
    colormapping(data, legend_kwargs, ax)


def edge_colormapping(
    G: nx.Graph,
    color_by: Hashable,
    legend_kwargs: Dict = {"loc": "lower right", "bbox_to_anchor": (0.0, 0.0)},
    ax=None,
):
    """Annotate edge color mapping."""
    if ax is None:
        ax = plt.gca()
    et = utils.edge_table(G)
    data = et[color_by]
    colormapping(data, legend_kwargs, ax)


def node_labels(G, layout_func, group_by, sort_by, fontdict={}, ax=None):
    """Annotate node labels."""
    validate_fontdict(fontdict)
    if ax is None:
        ax = plt.gca()

    nt = utils.node_table(G)
    pos = layout_func(nt, group_by, sort_by)
    for node in G.nodes():
        ax.annotate(text=node, xy=pos[node], ha="center", va="center", **fontdict)


def circos_labels(
    G: nx.Graph,
    group_by: Hashable = None,
    sort_by: Hashable = None,
    layout: str = "node_center",
    radius: float = None,
    radius_offset: float = 1,
    fontdict: Dict = {},
    ax=None,
):
    """Annotate node labels for circos plot."""
    assert layout in ("node_center", "standard", "rotate", "numbers")
    if layout == "node_center":
        return node_labels(G, layouts.circos, group_by, sort_by, fontdict)

    validate_fontdict(fontdict)
    if ax is None:
        ax = plt.gca()

    nt = utils.node_table(G, group_by, sort_by)
    nodes = list(nt.index)

    if radius is None:
        radius = circos_radius(len(nodes))

    if layout == "numbers":
        radius_adjustment = radius / (radius + radius_offset)
    else:
        radius_adjustment = 1.02
    radius += radius_offset

    for i, (node, data) in enumerate(nt.iterrows()):
        theta = item_theta(nodes, node)
        x, y = to_cartesian(r=radius * radius_adjustment, theta=theta)
        ha, va = text_alignment(x, y)

        if layout == "numbers":
            tx, _ = to_cartesian(r=radius, theta=theta)
            tx *= 1 - np.log(np.cos(theta) * utils.nonzero_sign(np.cos(theta)))
            tx += utils.nonzero_sign(x)

            ty_numerator = (
                2
                * radius
                * (theta % (utils.nonzero_sign(y) * utils.nonzero_sign(x) * np.pi))
            )
            ty_denominator = utils.nonzero_sign(x) * np.pi
            ty = ty_numerator / ty_denominator

            ax.annotate(
                text="{} - {}".format(*((i, node) if (x > 0) else (node, i))),
                xy=(tx, ty),
                ha=ha,
                va=va,
                **fontdict,
            )
            ax.annotate(text=i, xy=(x, y), ha="center", va="center")

        elif layout == "rotate":
            theta_deg = to_degrees(theta)
            if -90 <= theta_deg <= 90:
                rot = theta_deg
            else:
                rot = theta_deg - 180
            ax.annotate(
                text=node,
                xy=(x, y),
                ha=ha,
                va="center",
                rotation=rot,
                rotation_mode="anchor",
                **fontdict,
            )

        # Standard layout
        else:
            ax.annotate(text=node, xy=(x, y), ha=ha, va=va, **fontdict)


def arc_labels(
    G: nx.Graph,
    group_by: Hashable = None,
    sort_by: Hashable = None,
    layout: str = "node_center",
    y_offset: float = -1,
    ha: str = "right",
    va: str = "top",
    rotation: float = 45,
    fontdict: Dict = {},
    ax=None,
):
    """Annotate node labels for arc plot."""
    assert layout in ("node_center", "standard")
    if layout == "node_center":
        return node_labels(G, layouts.arc, group_by, sort_by, fontdict)

    validate_fontdict(fontdict)
    if ax is None:
        ax = plt.gca()

    nt = utils.node_table(G, group_by, sort_by)

    for x, (node, data) in enumerate(nt.iterrows()):
        ax.annotate(
            node,
            xy=(x * 2, y_offset),
            ha=ha,
            va=va,
            rotation=rotation,
            **fontdict,
        )


def matrix_labels(
    G: nx.Graph,
    group_by: Hashable = None,
    sort_by: Hashable = None,
    layout: str = "node_center",
    offset: float = -1.5,
    x_ha: str = "right",
    x_va: str = "top",
    y_ha: str = "right",
    y_va: str = "center",
    x_rotation: float = 45,
    y_rotation: float = 0,
    fontdict: Dict = {},
    ax=None,
):
    """Annotate node labels for matrix plot."""
    assert layout in ("node_center", "standard")
    validate_fontdict(fontdict)
    if ax is None:
        ax = plt.gca()

    nt = utils.node_table(G, group_by, sort_by)

    if layout == "node_center":
        x_ha = "center"
        x_va = "center"
        y_ha = "center"
        y_va = "center"
        offset = 0
        x_rotation = 0
        y_rotation = 0

    for i, (node, data) in enumerate(nt.iterrows()):
        position = (i + 1) * 2

        # Plot the x-axis labels
        ax.annotate(
            node,
            xy=(position, offset),
            ha=x_ha,
            va=x_va,
            rotation=x_rotation,
            **fontdict,
        )

        # Plot the y-axis labels
        ax.annotate(
            node,
            xy=(offset, position),
            ha=y_ha,
            va=y_va,
            rotation=y_rotation,
            **fontdict,
        )


parallel_labels = partial(node_labels, layout_func=layouts.parallel, sort_by=None)
update_wrapper(parallel_labels, node_labels)
parallel_labels.__name__ = "annotate.parallel_labels"

hive_labels = partial(node_labels, layout_func=layouts.hive, sort_by=None)
update_wrapper(hive_labels, node_labels)
hive_labels.__name__ = "annotate.hive_labels"
