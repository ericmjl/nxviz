from hypothesis import given, assume
from hypothesis.strategies import lists, integers, floats, tuples
import numpy as np
import nxviz as nv
from nxviz.base import BasePlot
from nxviz import circos
from nxviz import geometry as gm
import pytest


@given(lists(integers()), integers())
def test_node_theta(nodelist, node):
    assume(len(nodelist) > 0)
    assume(node in nodelist)
    theta_obs = gm.node_theta(nodelist, node)

    i = nodelist.index(node)
    theta_exp = i*2*np.pi/len(nodelist)

    assert np.allclose(theta_obs, theta_exp)


@given(floats(), floats())
def test_get_cartesian(r, theta):
    assume(np.isfinite(theta))
    assume(np.isfinite(r))
    x_obs, y_obs = gm.get_cartesian(r, theta)
    x_exp = r * np.sin(theta)
    y_exp = r * np.cos(theta)

    assert np.allclose(x_obs, x_exp)
    assert np.allclose(y_obs, y_exp)


@given(floats())
def test_correct_negative_angle(angle):

    assume(angle < 0)
    assume(angle >= -2 * np.pi)
    exp = 2 * np.pi + angle
    obs = gm.correct_negative_angle(angle)

    assert np.allclose(obs, exp)
    assert obs <= 2 * np.pi
    assert obs >= 0

@given(lists(integers(), unique=True),
       lists(integers(), unique=True, min_size=2, max_size=2))
def test_initialization(nodes, edges):
    assume(len(nodes) > 2 and len(nodes) < 5)
    assume(len(edges) > 1 and len(edges) < 5)
    b = BasePlot(nodes, edges)
    assert b.nodecolors == ['blue'] * len(b.nodes)
    assert b.edgecolors == ['black'] * len(b.edges)
