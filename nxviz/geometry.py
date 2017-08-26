"""
Utility geometry functions that can help with drawing to screen.
"""
import numpy as np

from .polcart import to_cartesian


def node_theta(nodelist, node):
    """
    Maps node to Angle.

    :param nodelist: Nodelist from the graph.
    :type nodelist: list.
    :param node: The node of interest. Must be in the nodelist.
    :returns: theta -- the angle of the node in radians.
    """
    assert len(nodelist) > 0, 'nodelist must be a list of items.'
    assert node in nodelist, 'node must be inside nodelist.'

    i = nodelist.index(node)
    theta = -np.pi + i*2*np.pi/len(nodelist)

    return theta


def get_cartesian(r, theta):
    """
    Returns the cartesian (x,y) coordinates of (r, theta).

    :param r: Real-valued radius.
    :type r: int, float.
    :param theta: Angle
    :type theta: int, float.
    :returns: to_cartesian(r, theta)
    """
    return to_cartesian(r, theta)


def correct_negative_angle(angle):
    """
    Corrects a negative angle to a positive one.

    :param angle: The angle in radians.
    :type angle: float
    :returns: `angle`, corrected to be positively-valued.
    """
    if angle < 0:
        angle = 2 * np.pi + angle
    else:
        pass

    return angle


def circos_radius(n_nodes, node_r):
    """
    Automatically computes the origin-to-node centre radius of the Circos plot
    using the triangle equality sine rule.

    a / sin(A) = b / sin(B) = c / sin(C)

    :param n_nodes: the number of nodes in the plot.
    :type n_nodes: int
    :param node_r: the radius of each node.
    :type node_r: float
    :returns: Origin-to-node centre radius.
    """
    A = 2 * np.pi / n_nodes  # noqa
    B = (np.pi - A) / 2  # noqa
    a = 2 * node_r
    return a * np.sin(B) / np.sin(A)
