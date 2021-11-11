"""
Utility geometry functions that can help with drawing to screen.
"""
import numpy as np

from .polcart import to_cartesian
from typing import List, Hashable


def item_theta(itemlist: List[Hashable], item: Hashable):
    """
    Maps node to an angle in radians.

    :param itemlist: Item list from the graph.
    :param item: The item of interest. Must be in the itemlist.
    :returns: theta -- the angle of the item in radians.
    """
    assert len(itemlist) > 0, "itemlist must be a list of items."
    assert item in itemlist, "item must be inside itemlist."

    i = itemlist.index(item)
    theta = i * 2 * np.pi / len(itemlist)

    return theta


def get_cartesian(r: float, theta: float):
    """
    Returns the cartesian (x,y) coordinates of (r, theta).

    :param r: Real-valued radius.
    :param theta: Angle in radians.
    :returns: to_cartesian(r, theta)
    """
    return to_cartesian(r, theta)


def correct_negative_angle(angle):
    """
    Corrects a negative angle to a positive one.

    :param angle: The angle in radians.
    :returns: `angle`, corrected to be positively-valued.
    """
    angle = angle % (2 * np.pi)
    if angle < 0:
        angle += 2 * np.pi
    return angle


def circos_radius(n_nodes: int, node_radius: float = 1.0):
    """
    Automatically computes the origin-to-node centre radius of the Circos plot
    using the triangle equality sine rule.

    a / sin(A) = b / sin(B) = c / sin(C)

    :param n_nodes: the number of nodes in the plot.
    :param node_radius: the radius of each node.
    :returns: Origin-to-node centre radius.
    """
    A = 2 * np.pi / n_nodes  # noqa
    B = (np.pi - A) / 2  # noqa
    a = 2 * node_radius
    return a * np.sin(B) / np.sin(A)


def correct_hive_angles(start, end):
    """Perform correction of hive plot angles for edge drawing."""
    if start > np.pi and end == 0.0:
        end = 2 * np.pi
    if start < np.pi and end == 0.0:
        start, end = end, start
    if end < np.pi and start == 2 * np.pi:
        start = 0
    if end > np.pi and start == 0:
        start = 2 * np.pi
    return start, end
