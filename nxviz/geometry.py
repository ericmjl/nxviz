"""
Utility geometry functions that can help with drawing to screen.
"""
from polcart import to_cartesian
import numpy as np


def node_theta(nodelist, node):
    """
    Maps node to Angle.
    """
    assert len(nodelist) > 0, 'nodelist must be a list of items.'
    assert node in nodelist, 'node must be inside nodelist.'

    i = nodelist.index(node)
    theta = -np.pi + i*2*np.pi/len(nodelist)

    return theta


def get_cartesian(r, theta):
    """
    Returns the cartesian (x,y) coordinates of (r, theta).
    """
    return to_cartesian(r, theta)


def correct_negative_angle(angle):
    """
    Corrects a negative angle to a positive one.
    """
    if angle < 0:
        angle = 2 * np.pi + angle
    else:
        pass

    return angle


def circos_radius(n_nodes, node_r):
    """
    Automatically cmputes the origin-to-node centre radius of the Circos plot
    using the triangle equality sine rule.

    a / sin(A) == b / sin(B) == c / sin(C)

    n_nodes: the number of nodes in the plot.
    node_r: the radius of each node.
    """
    A = 2 * np.pi / n_nodes
    B = (np.pi - A) / 2
    a = 2 * node_r
    return a * np.sin(B) / np.sin(A)
