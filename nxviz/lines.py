"""Patch generators for edges."""


from itertools import product
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Circle, Patch, Path, PathPatch

from nxviz.geometry import correct_hive_angles
from nxviz.polcart import to_cartesian, to_polar, to_radians


def circos(
    et: pd.DataFrame,
    pos: Dict,
    edge_color: Iterable,
    alpha: Iterable,
    lw: Iterable,
    aes_kw: Dict,
) -> List[Patch]:
    """Circos plot line drawing."""
    patches = []
    for r, d in et.iterrows():
        verts = [pos[d["source"]], (0, 0), pos[d["target"]]]
        codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        path = Path(verts, codes)
        patch = PathPatch(
            path, edgecolor=edge_color[r], alpha=alpha[r], lw=lw[r], **aes_kw
        )
        patches.append(patch)
    return patches


def line(
    et: pd.DataFrame,
    pos: Dict,
    edge_color: Iterable,
    alpha: Iterable,
    lw: Iterable,
    aes_kw: Dict,
):
    """Straight line drawing function."""
    patches = []
    for r, d in et.iterrows():
        start = d["source"]
        end = d["target"]
        verts = [pos[start], pos[end]]
        codes = [Path.MOVETO, Path.LINETO]
        path = Path(verts, codes)
        patch = PathPatch(
            path, edgecolor=edge_color[r], alpha=alpha[r], lw=lw[r], **aes_kw
        )
        patches.append(patch)
    return patches


def arc(
    et: pd.DataFrame,
    pos: Dict,
    edge_color: Iterable,
    alpha: Iterable,
    lw: Iterable,
    aes_kw: Dict,
):
    """Arc plot edge drawing function."""
    patches = []
    for r, d in et.iterrows():
        start = d["source"]
        end = d["target"]
        start_x, start_y = pos[start]
        end_x, end_y = pos[end]

        middle_x = np.mean([start_x, end_x])
        middle_y = np.mean([start_y, end_y])

        width = abs(end_x - start_x)
        height = width

        r1, theta1 = to_polar(start_x - middle_x, start_y - middle_y)
        r2, theta2 = to_polar(end_x - middle_x, end_y - middle_y)

        theta1 = np.rad2deg(theta1)
        theta2 = np.rad2deg(theta2)

        theta1, theta2 = min([theta1, theta2]), max([theta1, theta2])

        patch = Arc(
            xy=(middle_x, middle_y),
            width=width,
            height=height,
            theta1=theta1,
            theta2=theta2,
            edgecolor=edge_color[r],
            alpha=alpha[r],
            lw=lw[r],
            **aes_kw,
        )
        patches.append(patch)
    return patches


def hive(
    et: pd.DataFrame,
    pos: Dict,
    pos_cloned: Dict,
    edge_color: Iterable,
    alpha: Iterable,
    lw: Iterable,
    aes_kw: Dict,
    curves: bool = True,
):
    """Hive plot line drawing function."""
    rad = pd.Series(pos).apply(lambda val: to_polar(*val)).to_dict()
    if pos_cloned is None:
        pos_cloned = pos
    rad_cloned = pd.Series(pos_cloned).apply(lambda val: to_polar(*val)).to_dict()

    patches = []
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
        patch = PathPatch(
            path, lw=lw[r], alpha=alpha[r], edgecolor=edge_color[r], **aes_kw
        )
        patches.append(patch)
    return patches


def matrix(
    et,
    pos,
    pos_cloned,
    edge_color: Iterable,
    alpha: Iterable,
    lw: Iterable,
    aes_kw: Dict,
):
    """Matrix plot edge drawing function."""
    patches = []
    for r, d in et.iterrows():
        start = d["source"]
        end = d["target"]
        x_start, y_start = pos_cloned[start]
        x_end, y_end = pos[end]

        x, y = (max(x_start, y_start), max(x_end, y_end))
        kw = {
            "fc": edge_color[r],
            "alpha": alpha[r],
            "radius": lw[r],
            "zorder": 1,
        }
        kw.update(aes_kw)
        patch = Circle(xy=(x, y), **kw)
        patches.append(patch)
    return patches
