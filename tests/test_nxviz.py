"""Tests for nxviz high level API."""

from itertools import cycle
from matplotlib import pyplot as plt

import nxviz as nv

import pytest


@pytest.mark.usefixtures("dummyG")
def test_api(dummyG):
    """Tests that the high level APIs work properly."""
    apifuncs = nv.arc, nv.circos, nv.parallel, nv.hive, nv.matrix

    for func in apifuncs:
        fig, ax = plt.subplots()
        func(dummyG, group_by="group", sort_by="value", edge_alpha_by="edge_value")
