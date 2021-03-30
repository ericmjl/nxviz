"""Integration tests that operate at the mid-level API."""


from nxviz import nodes, edges
import pytest


@pytest.mark.usefixtures("dummyG")
def test_hive_no_clone(dummyG):
    """Test for hive plot with no cloning of axes."""
    pos = nodes.hive(dummyG, group_by="group")

    edges.hive(dummyG, pos, pos_cloned=None)
