"""
Utility geometry functions that can help with drawing to screen.
"""

import numpy as np


def node_theta(nodelist, node):
    """
    Maps node to Angle.
    """
    i = nodelist.index(node)
    theta = i*2*np.pi/len(nodelist)

    return theta


def get_cartesian(r, theta):
    """
    Returns the cartesian (x,y) coordinates of (r, theta).
    """
    x = r*np.sin(theta)
    y = r*np.cos(theta)

    return x, y


def correct_negative_angle(angle):
    """
    Corrects a negative angle to a positive one.
    """
    if angle < 0:
        angle = 2 * np.pi + angle
    else:
        pass

    return angle
