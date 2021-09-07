"""Tests for nxviz high level API."""

from itertools import cycle
from matplotlib import pyplot as plt

import nxviz as nv

import pytest


@pytest.mark.usefixtures("dummyG")
@pytest.mark.parametrize("alpha_bounds", [(None,), ((0, 1),)])
def test_api(dummyG, alpha_bounds):
    """Tests that the high level APIs work properly."""
    apifuncs = nv.arc, nv.circos, nv.parallel, nv.hive, nv.matrix
    encodings_kwargs = {"alpha_bounds": alpha_bounds}
    for func in apifuncs:
        fig, ax = plt.subplots()
        func(dummyG, group_by="group", sort_by="value", edge_alpha_by="edge_value")


def test_classes(dummyG):
    """Tests that the object oriented APIs execute."""
    objects = nv.ArcPlot, nv.CircosPlot, nv.MatrixPlot, nv.HivePlot
    for obj in objects:
        fig, ax = plt.subplots()
        obj(dummyG, node_grouping="group", node_order="value", node_color="group")
