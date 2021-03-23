from copy import deepcopy
from typing import Dict

import janitor

import matplotlib.pyplot as plt
import networkx as nx

import pandas as pd
from datashader.bundling import hammer_bundle
from matplotlib import patches
from matplotlib.patches import Path

from .utils import edge_table

default_edge_kwargs = dict(alpha=0.1, facecolor="none", zorder=0)


def lw_func(d):
    """Return default line width."""
    return 1


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
    edgekw = update_default_edge_kwargs(edge_kwargs)
    ax = hb.plot(x="x", y="y", ax=ax, zorder=0, **edgekw)
    ax.legend().remove()


from nxviz import colors


def circos_curves(
    G: nx.Graph,
    pos: Dict,
    color_by=None,
    lw_func=lw_func,
    alpha_func=alpha_func,
    ax=None,
    edge_kwargs={},
):
    """Draw circos plot curves."""

    et = edge_table(G)
    edge_colors = ["black"] * len(et)
    if color_by:
        edge_colors = colors.data_color(et[color_by]).to_list()
    if ax is None:
        ax = plt.gca()
    edgekw = update_default_edge_kwargs(edge_kwargs)
    for i, (start, end, d) in enumerate(G.edges(data=True)):
        verts = [pos[start], (0, 0), pos[end]]
        codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        path = Path(verts, codes)
        edgekw.update(lw=lw_func(d), alpha=alpha_func(d), edgecolor=edge_colors[i])
        patch = patches.PathPatch(path, **edgekw)
        ax.add_patch(patch)


def lines(G: nx.Graph, pos: Dict, ax=None, edge_kwargs={}):
    """Vanilla lines between nodes.

    Can be used with almost any node layout.
    """
    if ax is None:
        ax = plt.gca()
    edgekw = update_default_edge_kwargs(edge_kwargs)

    for start, end in G.edges():
        verts = [pos[start], pos[end]]
        codes = [Path.MOVETO, Path.LINETO]
        path = Path(verts, codes)
        edgekw = update_default_edge_kwargs(edge_kwargs)
        patch = patches.PathPatch(path, **edgekw)
        ax.add_patch(patch)


import numpy as np


def arc_curves(
    G: nx.Graph,
    pos: Dict,
    color_by=None,
    lw_func=lw_func,
    alpha_func=alpha_func,
    edge_kwargs: Dict = {},
    ax=None,
):
    """ArcPlot curves."""

    et = edge_table(G)
    edge_colors = ["black"] * len(et)
    if color_by:
        edge_colors = colors.data_color(et[color_by]).to_list()

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
            {"lw": lw_func(d), "alpha": alpha_func(d), "edgecolor": edge_colors[i]}
        )
        patch = patches.Arc(
            xy=(middle_x, middle_y),
            width=width,
            height=height,
            theta1=theta1,
            theta2=theta2,
            **edgekw
        )
        ax.add_patch(patch)


from itertools import product

from nxviz.geometry import correct_hive_angles
from nxviz.polcart import to_cartesian, to_polar, to_radians


def hive(
    G: nx.Graph,
    pos: Dict,
    pos_cloned: Dict = None,
    color_by=None,
    lw_func=lw_func,
    alpha_func=alpha_func,
    curves: bool = True,
    edge_kwargs={},
    ax=None,
):
    """Draw hive plot edges to a matplotlib axes object."""

    et = edge_table(G)
    edge_colors = ["black"] * len(et)
    if color_by:
        edge_colors = colors.data_color(et[color_by]).to_list()

    rad = pd.Series(pos).apply(lambda val: to_polar(*val)).to_dict()
    if pos_cloned is None:
        pos_cloned = pos
    rad_cloned = pd.Series(pos_cloned).apply(lambda val: to_polar(*val)).to_dict()

    if ax is None:
        ax = plt.gca()

    edgekw = update_default_edge_kwargs(edge_kwargs)
    for i, (start, end, d) in enumerate(G.edges(data=True)):
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
        edgekw.update(lw=lw_func(d), alpha=alpha_func(d), edgecolor=edge_colors[i])
        patch = patches.PathPatch(path, **edgekw)
        ax.add_patch(patch)
