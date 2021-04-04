"""Node layout engines.

Compatible with NetworkX's drawing facilities;
they will each return a dictionary
of node mapped to a cartesian coordinate on the (x, y) plane.
"""

from typing import Dict, Hashable

import numpy as np
import pandas as pd

from nxviz.geometry import circos_radius, item_theta
from nxviz.polcart import to_cartesian
from nxviz.utils import group_and_sort


def parallel(
    nt: pd.DataFrame, group_by: Hashable, sort_by: Hashable = None
) -> Dict[Hashable, np.ndarray]:
    """Parallel coordinates node layout."""
    pos = dict()

    for x, (grp, data) in enumerate(nt.groupby(group_by)):
        if sort_by is not None:
            data = data.sort_values(sort_by)
        for y, (node, d) in enumerate(data.iterrows()):
            pos[node] = np.array([x * 4, y])
    return pos


def circos(
    nt: pd.DataFrame,
    group_by: Hashable = None,
    sort_by: Hashable = None,
    radius: float = None,
) -> Dict[Hashable, np.ndarray]:
    """Circos plot node layout."""
    pos = dict()
    nt = group_and_sort(nt, group_by, sort_by)
    nodes = list(nt.index)
    if radius is None:
        radius = circos_radius(len(nodes))
    if group_by:
        for grp, df in nt.groupby(group_by):
            for node, data in df.iterrows():
                x, y = to_cartesian(r=radius, theta=item_theta(nodes, node))
                pos[node] = np.array([x, y])
    else:
        for node, data in nt.iterrows():
            x, y = to_cartesian(r=radius, theta=item_theta(nodes, node))
            pos[node] = np.array([x, y])
    return pos


def hive(
    nt: pd.DataFrame,
    group_by,
    sort_by: Hashable = None,
    inner_radius: float = 8,
    rotation: float = 0,
):
    """Hive plot node layout.

    ## Parameters

    - `inner_radius`: The inner
    """
    nt = group_and_sort(nt, group_by=group_by, sort_by=sort_by)
    groups = sorted(nt[group_by].unique())
    if len(groups) > 3:
        raise ValueError(
            f"group_by {group_by} is associated with more than 3 groups. "
            f"The groups are {groups}. "
            "Hive plots can only handle at most 3 groups at a time."
        )
    pos = dict()
    for grp, df in nt.groupby(group_by):
        for i, (node, data) in enumerate(df.iterrows()):
            radius = inner_radius + i
            theta = item_theta(groups, grp) + rotation
            x, y = to_cartesian(r=radius * 2, theta=theta)
            pos[node] = np.array([x, y])
    return pos


def arc(nt, group_by: Hashable = None, sort_by: Hashable = None):
    """Arc plot node layout."""
    nt = group_and_sort(nt, group_by=group_by, sort_by=sort_by)
    pos = dict()
    for x, (node, data) in enumerate(nt.iterrows()):
        pos[node] = np.array([x * 2, 0])
    return pos


def geo(nt, group_by=None, sort_by=None, longitude="longitude", latitude="latitude"):
    """Geographical node layout."""
    pos = dict()
    for node, data in nt.iterrows():
        pos[node] = data[[longitude, latitude]]
    return pos


def matrix(nt, group_by: Hashable = None, sort_by: Hashable = None, axis="x"):
    """Matrix plot layout."""
    # Nodes should be grouped and sorted before we begin assigning coordinates.
    nt = group_and_sort(node_table=nt, group_by=group_by, sort_by=sort_by)

    # We are eventually going to return this pos dictionary.
    pos = dict()

    # Loop over each of the rows, and assign x, y coordinates in order of them being grouped and sorted.
    for i, (node, data) in enumerate(nt.iterrows()):
        x = (i + 1) * 2
        y = 0

        if axis == "y":
            x, y = y, x
        pos[node] = np.array([x, y])
    return pos
