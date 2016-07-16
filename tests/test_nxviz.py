from hypothesis import given, assume
from hypothesis.strategies import lists, integers, floats
import numpy as np
import nxviz as nv
from nxviz import base
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
