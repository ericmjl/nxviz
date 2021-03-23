"""Functions for drawing edges.

In drawing edges, we need to know some pieces of information beforehand.

Firstly,
"""

from copy import deepcopy
from itertools import product
from typing import Dict, Hashable, Callable

import janitor
import matplotlib.pyplot as plt
import networkx as nx
from networkx.generators import line
import numpy as np
import pandas as pd
from datashader.bundling import hammer_bundle
from matplotlib.patches import Path, PathPatch, Arc

from . import colors
from .geometry import correct_hive_angles
from .polcart import to_cartesian, to_polar, to_radians
from .utils import edge_table

default_edge_kwargs = dict(facecolor="none", zorder=0)


def alpha_func(d):
    """Return default transparency."""
    return 0.1


def color_func(d):
    """Return default color."""
    return "black"


def update_default_edge_kwargs(edge_kwargs):
    edgekw = deepcopy(default_edge_kwargs)
    edgekw.update(edge_kwargs)
    return edgekw


def edge_colors(et: pd.DataFrame, color_by: Hashable):
    edge_color = ["black"] * len(et)
    if color_by:
        edge_color = colors.data_color(et[color_by])
    return edge_color


def bundle(G, pos, ax=None, edge_kwargs={}):
    edge_df = edge_table(G)
    node_df = (
        pd.DataFrame(pos)
        .T.reset_index()
        .rename_columns({0: "x", 1: "y", "index": "name"})
    )
    hb = hammer_bundle(nodes=node_df, edges=edge_df)
    if ax is None:
        ax = plt.gca()
    ax = hb.plot(x="x", y="y", ax=ax)
    ax.legend().remove()


from . import lines


def line_width(et: pd.DataFrame, lw_by: Hashable, lw_func: Callable):
    if lw_by is not None:
        return et[lw_by].apply(lw_func)
    return pd.Series([1] * len(et))


def transparency(et: pd.DataFrame, alpha_by: Hashable, alpha_func: Callable):
    if alpha_by is not None:
        return et[alpha_by].apply(alpha_func)
    return pd.Series([1] * len(et))


def circos(
    G: nx.Graph,
    pos: Dict,
    color_by=None,
    lw_by=None,
    lw_func=lambda _: 1,
    alpha_by=None,
    alpha_func=lambda _: 0.1,
    ax=None,
    edge_kwargs={},
):
    """Draw circos plot curves."""
    et = edge_table(G)
    if ax is None:
        ax = plt.gca()
    edgekw = update_default_edge_kwargs(edge_kwargs)

    edge_color = edge_colors(et, color_by)
    lw = line_width(et, lw_by, lw_func)
    alpha = transparency(et, alpha_by, alpha_func)

    patches = lines.circos(
        et, pos, edge_color=edge_color, alpha=alpha, lw=lw, edge_kwargs=edgekw
    )
    for patch in patches:
        ax.add_patch(patch)


def line(
    G: nx.Graph,
    pos: Dict,
    color_by=None,
    lw_by=None,
    lw_func=lambda _: 1,
    alpha_by=None,
    alpha_func=lambda _: 0.1,
    ax=None,
    edge_kwargs={},
):
    """Vanilla lines between nodes.

    Can be used with almost any node layout.
    """
    et = edge_table(G)
    if ax is None:
        ax = plt.gca()
    edgekw = update_default_edge_kwargs(edge_kwargs)

    edge_color = edge_colors(et, color_by)
    lw = line_width(et, lw_by, lw_func)
    alpha = transparency(et, alpha_by, alpha_func)
    patches = lines.line(et, pos, edge_color, alpha, lw, edgekw)
    for patch in patches:
        ax.add_patch(patch)


def arc(
    G: nx.Graph,
    pos: Dict,
    color_by=None,
    lw_func=lambda _: 1,
    alpha_func=alpha_func,
    edge_kwargs: Dict = {},
    ax=None,
):
    """ArcPlot curves."""

    et = edge_table(G)
    edge_color = edge_colors(et, color_by)
    if ax is None:
        ax = plt.gca()
    edgekw = update_default_edge_kwargs(edge_kwargs)

    for i, (start, end, d) in enumerate(G.edges(data=True)):
        start_x, start_y = pos[start]
        end_x, end_y = pos[end]

        middle_x = np.mean([start_x, end_x])
        middle_y = np.mean([start_y, end_y])

        width = abs(end_x - start_x)
        height = width

        theta1, theta2 = 0, 180
        edgekw.update(
            {"lw": lw_func(d), "alpha": alpha_func(d), "edgecolor": edge_color[i]}
        )
        patch = Arc(
            xy=(middle_x, middle_y),
            width=width,
            height=height,
            theta1=theta1,
            theta2=theta2,
            **edgekw
        )
        ax.add_patch(patch)


def hive(
    G: nx.Graph,
    pos: Dict,
    pos_cloned: Dict = None,
    color_by=None,
    lw_func=lambda _: 1,
    alpha_func=alpha_func,
    curves: bool = True,
    edge_kwargs={},
    ax=None,
):
    """Draw hive plot edges to a matplotlib axes object."""

    et = edge_table(G)
    edge_color = edge_colors(et, color_by)
    if ax is None:
        ax = plt.gca()
    edgekw = update_default_edge_kwargs(edge_kwargs)

    rad = pd.Series(pos).apply(lambda val: to_polar(*val)).to_dict()
    if pos_cloned is None:
        pos_cloned = pos
    rad_cloned = pd.Series(pos_cloned).apply(lambda val: to_polar(*val)).to_dict()

    for r, d in et.iterrows():
        start = d["source"]
        end = d["target"]
        start_radius, start_theta = rad[start]
        end_radius, end_theta = rad[end]

        _, start_theta_cloned = rad_cloned[start]
        _, end_theta_cloned = rad_cloned[end]

        # Find the pair of start and end thetas that give the smallest acute angle
        smallest_pair = None
        smallest_nonzero_angle = np.inf
        starts = [start_theta, start_theta_cloned]
        ends = [end_theta, end_theta_cloned]

        for start, end in product(starts, ends):
            start, end = correct_hive_angles(start, end)
            if not np.allclose(end - start, 0):
                angle = to_radians(abs(min([end - start, start - end])))
                if angle < smallest_nonzero_angle:
                    smallest_nonzero_angle = abs(angle)
                    smallest_pair = ((start_radius, start), (end_radius, end))

        if smallest_pair is None:
            continue

        (start_radius, start_theta), (end_radius, end_theta) = smallest_pair
        if np.allclose(end_theta, 0):
            end_theta = 2 * np.pi
        startx, starty = to_cartesian(start_radius, start_theta)
        endx, endy = to_cartesian(end_radius, end_theta)

        middle_theta = np.mean([start_theta, end_theta])

        middlex1, middley1 = to_cartesian(start_radius, middle_theta)
        middlex2, middley2 = to_cartesian(end_radius, middle_theta)
        endx, endy = to_cartesian(end_radius, end_theta)

        verts = [(startx, starty), (endx, endy)]
        codes = [Path.MOVETO, Path.LINETO]
        if curves:
            verts = [
                (startx, starty),
                (middlex1, middley1),
                (middlex2, middley2),
                (endx, endy),
            ]
            codes = [
                Path.MOVETO,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
            ]

        path = Path(verts, codes)
        edgekw.update(lw=lw_func(d), alpha=alpha_func(d), edgecolor=edge_color[r])
        patch = PathPatch(path, **edgekw)
        ax.add_patch(patch)
