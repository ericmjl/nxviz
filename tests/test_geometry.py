from nxviz.geometry import (circos_radius, node_theta, get_cartesian,
                            correct_negative_angle)
from hypothesis import given, assume
from hypothesis.strategies import lists, integers, floats
import numpy as np
import pytest


def test_circos_radius():
    """
    Uses the other triangle geometry rule to check that the radius is correct.
    """

    n_nodes = 10
    node_r = 1

    A = 2 * np.pi / n_nodes

    circ_r = 2 * node_r / np.sqrt(2 * (1 - np.cos(A)))

    assert np.allclose(circ_r, circos_radius(n_nodes, node_r))


@given(lists(integers()), integers())
def test_node_theta(nodelist, node):
    """
    Tests node_theta function.
    """
    assume(len(nodelist) > 0)
    assume(node in nodelist)
    theta_obs = node_theta(nodelist, node)

    i = nodelist.index(node)
    theta_exp = i*2*np.pi/len(nodelist)
    if theta_exp > np.pi:
        theta_exp = np.pi - theta_exp
    assert np.allclose(theta_obs, theta_exp)


@given(floats(), floats())
@pytest.mark.skip(reason="tested in polcart")
def test_get_cartesian(r, theta):
    assume(np.isfinite(theta))
    assume(np.isfinite(r))
    x_obs, y_obs = get_cartesian(r, theta)
    x_exp = r * np.sin(theta)
    y_exp = r * np.cos(theta)

    assert np.allclose(x_obs, x_exp)
    assert np.allclose(y_obs, y_exp)


@given(floats())
def test_correct_negative_angle(angle):

    assume(angle < 0)
    assume(angle >= -2 * np.pi)
    exp = 2 * np.pi + angle
    obs = correct_negative_angle(angle)

    assert np.allclose(obs, exp)
    assert obs <= 2 * np.pi
    assert obs >= 0
