"""
Utility geometry functions that can help with drawing to screen.
"""

import numpy as np
from polcart import to_cartesian


def node_theta(nodelist, node):
    """
    Maps node to Angle.
    """
    assert len(nodelist) > 0, 'nodelist must be a list of items.'
    assert node in nodelist, 'node must be inside nodelist.'

    i = nodelist.index(node)
    theta = i*2*np.pi/len(nodelist)

    return theta


def get_cartesian(r, theta):
    """
    Wrapper function for to_cartesian from polcart. Takes advantage of all the
    angle value checking that polcart offers.

    We currently do this wrapping to minimize the changes that are needed in
    the rest of the codebase.
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
