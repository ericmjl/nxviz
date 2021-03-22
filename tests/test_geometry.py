"""Tests for geometry module."""

import numpy as np
from random import choice

import nxviz.polcart as polcart
from hypothesis import assume, given, settings
from hypothesis.strategies import floats, integers, lists
from nxviz.geometry import (
    circos_radius,
    correct_negative_angle,
    get_cartesian,
    item_theta,
)


def test_circos_radius():
    """
    Check radius correctness.

    Uses the other triangle geometry rule to check that the radius is correct.
    """
    n_nodes = 10
    node_r = 1

    A = 2 * np.pi / n_nodes  # noqa

    circ_r = 2 * node_r / np.sqrt(2 * (1 - np.cos(A)))

    assert np.allclose(circ_r, circos_radius(n_nodes, node_r))


# @settings(perform_health_check=False)
@given(lists(integers()))
def test_item_theta(nodelist):
    """Tests item_theta function."""
    assume(len(nodelist) > 0)
    node = choice(nodelist)
    theta_obs = item_theta(nodelist, node)

    i = nodelist.index(node)
    theta_exp = -np.pi + i * 2 * np.pi / len(nodelist)
    if theta_exp > np.pi:
        theta_exp = np.pi - theta_exp
    assert np.allclose(theta_obs, theta_exp)


@given(floats(), floats())
def test_get_cartesian(r, theta):
    """
    Test for get_cartesian.

    Makes sure that `get_cartesian` remains a wrapper around polcart's
    `to_cartesian`.
    """
    assume(np.isfinite(theta))
    assume(np.isfinite(r))
    assert get_cartesian(r, theta) == polcart.to_cartesian(r, theta)


# @settings(perform_health_check=False)
@given(floats())
def test_correct_negative_angle(angle):
    """Test for correct calculation of negative angle."""
    assume(angle < 0)
    assume(angle >= -2 * np.pi)
    exp = 2 * np.pi + angle
    obs = correct_negative_angle(angle)

    assert np.allclose(obs, exp)
    assert obs <= 2 * np.pi
    assert obs >= 0
