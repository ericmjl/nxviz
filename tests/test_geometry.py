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

tau = 2 * np.pi


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
    theta_observed = item_theta(nodelist, node)

    theta_expected = nodelist.index(node) / len(nodelist) * tau

    assert np.allclose(theta_observed, theta_expected)


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
@given(floats(max_value=0, min_value=-tau, exclude_max=True))
def test_correct_negative_angle(angle):
    """Test for correct calculation of negative angle."""
    exp = 2 * np.pi + angle
    obs = correct_negative_angle(angle)

    assert np.allclose(obs, exp)
    assert obs <= 2 * np.pi
    assert obs >= 0
