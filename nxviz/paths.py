"""Backend-agnostic edge path coordinate computation.

Each function returns a list of numpy arrays.
Each array has shape (N, 2) representing (x, y) control points for one edge.
These coordinates can be rendered by any backend (matplotlib, plotly, etc.).
"""

from itertools import product
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from nxviz.geometry import correct_hive_angles
from nxviz.polcart import to_cartesian, to_polar, to_radians


def circos_coords(et: pd.DataFrame, pos: Dict) -> List[np.ndarray]:
    """Circos edge path coordinates.

    Returns list of arrays, each shape (3, 2):
    [source_xy, center_0_0, target_xy] — quadratic Bezier control points.
    """
    coords = []
    for _, d in et.iterrows():
        src = np.array(pos[d["source"]])
        tgt = np.array(pos[d["target"]])
        center = np.array([0.0, 0.0])
        coords.append(np.array([src, center, tgt]))
    return coords


def line_coords(et: pd.DataFrame, pos: Dict) -> List[np.ndarray]:
    """Straight line edge path coordinates.

    Returns list of arrays, each shape (2, 2): [source_xy, target_xy].
    """
    coords = []
    for _, d in et.iterrows():
        src = np.array(pos[d["source"]])
        tgt = np.array(pos[d["target"]])
        coords.append(np.array([src, tgt]))
    return coords


def arc_coords(et: pd.DataFrame, pos: Dict, n_points: int = 50) -> List[np.ndarray]:
    """Arc edge path coordinates (discretized).

    Returns list of arrays, each shape (n_points, 2) representing
    evenly-spaced points along the semicircular arc between source and target.
    """
    coords = []
    for _, d in et.iterrows():
        start = d["source"]
        end = d["target"]
        start_x, start_y = pos[start]
        end_x, end_y = pos[end]

        middle_x = np.mean([start_x, end_x])
        middle_y = np.mean([start_y, end_y])

        radius = abs(end_x - start_x) / 2

        cx = middle_x
        cy = middle_y

        _, theta1 = to_polar(start_x - cx, start_y - cy)
        _, theta2 = to_polar(end_x - cx, end_y - cy)

        theta1_deg = np.rad2deg(theta1)
        theta2_deg = np.rad2deg(theta2)

        if theta1_deg > theta2_deg:
            theta1_deg, theta2_deg = theta2_deg, theta1_deg

        t = np.linspace(np.deg2rad(theta1_deg), np.deg2rad(theta2_deg), n_points)
        x = cx + radius * np.cos(t)
        y = cy + radius * np.sin(t)
        coords.append(np.column_stack([x, y]))
    return coords


def hive_coords(
    et: pd.DataFrame,
    pos: Dict,
    pos_cloned: Dict = None,
    curves: bool = True,
) -> List[np.ndarray]:
    """Hive plot edge path coordinates.

    When curves=True, returns list of arrays each shape (4, 2) — cubic Bezier.
    When curves=False, returns list of arrays each shape (2, 2) — straight lines.
    """
    if pos_cloned is None:
        pos_cloned = pos

    rad = pd.Series(pos).apply(lambda val: to_polar(*val)).to_dict()
    rad_cloned = pd.Series(pos_cloned).apply(lambda val: to_polar(*val)).to_dict()

    coords = []
    for _, d in et.iterrows():
        start = d["source"]
        end = d["target"]
        start_radius, start_theta = rad[start]
        end_radius, end_theta = rad[end]

        _, start_theta_cloned = rad_cloned[start]
        _, end_theta_cloned = rad_cloned[end]

        smallest_pair = None
        smallest_nonzero_angle = np.inf
        starts = [start_theta, start_theta_cloned]
        ends = [end_theta, end_theta_cloned]

        for s, e in product(starts, ends):
            s, e = correct_hive_angles(s, e)
            if not np.allclose(e - s, 0):
                angle = to_radians(abs(min([e - s, s - e])))
                if angle < smallest_nonzero_angle:
                    smallest_nonzero_angle = abs(angle)
                    smallest_pair = ((start_radius, s), (end_radius, e))

        if smallest_pair is None:
            coords.append(np.array([[0.0, 0.0], [0.0, 0.0]]))
            continue

        (sr, st), (er, et_theta) = smallest_pair
        if np.allclose(et_theta, 0):
            et_theta = 2 * np.pi
        startx, starty = to_cartesian(sr, st)
        endx, endy = to_cartesian(er, et_theta)

        middle_theta = np.mean([st, et_theta])

        if curves:
            middlex1, middley1 = to_cartesian(sr, middle_theta)
            middlex2, middley2 = to_cartesian(er, middle_theta)
            coords.append(
                np.array(
                    [
                        [startx, starty],
                        [middlex1, middley1],
                        [middlex2, middley2],
                        [endx, endy],
                    ]
                )
            )
        else:
            coords.append(np.array([[startx, starty], [endx, endy]]))
    return coords


def matrix_coords(
    et: pd.DataFrame,
    pos: Dict,
    pos_cloned: Dict,
) -> List[Tuple[float, float]]:
    """Matrix plot edge coordinates.

    Returns list of (x, y) tuples — the center position of each edge dot.
    """
    coords = []
    for _, d in et.iterrows():
        start = d["source"]
        end = d["target"]
        x_start, y_start = pos_cloned[start]
        x_end, y_end = pos[end]
        x = max(x_start, y_start)
        y = max(x_end, y_end)
        coords.append((x, y))
    return coords
