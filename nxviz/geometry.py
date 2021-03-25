"""
Utility geometry functions that can help with drawing to screen.
"""
import numpy as np

from .polcart import to_cartesian
from typing import List, Hashable


def item_theta(nodelist: List[Hashable], node: Hashable):
    """
    Maps node to Angle.

    :param nodelist: Nodelist from the graph.
    :param node: The node of interest. Must be in the nodelist.
    :returns: theta -- the angle of the node in radians.
    """
    assert len(nodelist) > 0, "nodelist must be a list of items."
    assert node in nodelist, "node must be inside nodelist."

    i = nodelist.index(node)
    theta = i * 2 * np.pi / len(nodelist)

    return theta


def group_theta(node_length, node_idx):
    """
    Returns an angle corresponding to a node of interest.

    Intended to be used for placing node group labels at the correct spot.

    :param float node_length: total number of nodes in the graph.
    :param int node_idx: the index of the node of interest.
    :returns: theta -- the angle of the node of interest in radians.
    """
    theta = -np.pi + node_idx * 2 * np.pi / node_length
    return theta


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


def correct_angles(start_radians, end_radians, rotation: float):
    """
    This function corrects for the following problems in the edges:
    """
    # Edges going the anti-clockwise direction involves angle = 0.
    if start_radians == 0 and (end_radians - start_radians > np.pi):
        start_radians = np.pi * 2
    if end_radians == 0 and (end_radians - start_radians < -np.pi):
        end_radians = np.pi * 2

    # Case when start_radians == end_radians:
    if start_radians == end_radians:
        start_radians = start_radians - rotation
        end_radians = end_radians + rotation
    return start_radians, end_radians


def circos_radius(n_nodes: int, node_radius: float = 1.0):
    """
    Automatically computes the origin-to-node centre radius of the Circos plot
    using the triangle equality sine rule.

    a / sin(A) = b / sin(B) = c / sin(C)

    :param n_nodes: the number of nodes in the plot.
    :param node_r: the radius of each node.
    :returns: Origin-to-node centre radius.
    """
    A = 2 * np.pi / n_nodes  # noqa
    B = (np.pi - A) / 2  # noqa
    a = 2 * node_radius
    return a * np.sin(B) / np.sin(A)


def correct_hive_angles(start, end):
    if start > np.pi and end == 0.0:
        end = 2 * np.pi
    if start < np.pi and end == 0.0:
        start, end = end, start
    if end < np.pi and start == 2 * np.pi:
        start = 0
    if end > np.pi and start == 0:
        start = 2 * np.pi
    return start, end
