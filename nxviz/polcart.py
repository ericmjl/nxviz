"""Polar/cartesian conversions functions."""

from numpy import arctan2 as atan2
from numpy import cos, pi, sin, sqrt


def to_cartesian(r, theta, proper=False):
    """
    Converts polar r, theta to cartesian x, y.
    """

    if proper:
        theta = to_proper_radians(theta)
    x = r * cos(theta)
    y = r * sin(theta)

    return x, y


import numpy as np


def to_polar(x, y):
    """
    Converts cartesian x, y to polar r, theta.
    """
    theta = atan2(y, x)
    r = sqrt(x ** 2 + y ** 2)

    if theta < 0:
        theta += 2 * np.pi

    return r, theta


def to_proper_radians(theta):
    """
    Converts theta (radians) to be within -pi and +pi.
    """
    if theta > pi or theta < -pi:
        theta = theta % pi
    return theta


def to_proper_degrees(theta):
    """
    Converts theta (degrees) to be within -180 and 180.
    """
    if theta > 180 or theta < -180:
        theta = theta % 180
    return theta


def to_degrees(theta):
    """
    Converts theta in radians to theta in degrees.
    """

    theta = to_proper_radians(theta)
    return theta / pi * 180


def to_radians(theta):
    """
    Converts theta in degrees to theta in radians.
    """
    theta = to_proper_degrees(theta)
    return theta * pi / 180
