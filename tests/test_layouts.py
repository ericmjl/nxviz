"""Tests for node layouts."""

from nxviz.utils import node_table
from nxviz import layouts
import pytest
import pandas as pd
import numpy as np


def get_pos_df(G, layout, group_by=None, sort_by=None, **layout_kwargs):
    """Convenience function to get position dictionary as a dataframe."""
    nt = node_table(G)
    pos = layout(nt, group_by, sort_by, **layout_kwargs)
    pos_df = pd.DataFrame(pos).T
    pos_df.columns = ["x", "y"]
    return pos_df, nt


@pytest.mark.usefixtures("dummyG")
@pytest.mark.parametrize("sort_by", ("value", None))
def test_parallel(dummyG, sort_by):
    """Test for parallel coordinates' plot.

    Checks:

    1. x-axis minimum position is at 0.
    2. x-axis maximum position is at 3 * num_groups - 1
    3. y-axis minimum position is at 0.
    """

    pos, nt = get_pos_df(dummyG, layouts.parallel, group_by="group", sort_by=sort_by)
    grp_lengths = nt.groupby("group").apply(lambda df: len(df))
    num_groups = len(grp_lengths)

    assert pos["x"].min() == 0
    assert pos["x"].max() == num_groups * 3 - 1
    assert pos["y"].min() == 0


@pytest.mark.usefixtures("dummyG")
@pytest.mark.parametrize("sort_by", ("value", None))
@pytest.mark.parametrize("group_by", ("group", None))
def test_circos(dummyG, group_by, sort_by):
    """Test for circos layout.

    Checks:

    1. Center of the circos layout is close to (0, 0).
    """
    pos, nt = get_pos_df(dummyG, layouts.circos, group_by=group_by, sort_by=sort_by)

    assert np.allclose(pos["x"].mean(), 0)
    assert np.allclose(pos["y"].mean(), 0)


@pytest.mark.usefixtures("dummyG")
@pytest.mark.parametrize("sort_by", ("value", None))
@pytest.mark.parametrize("group_by", ("group", None))
def test_arc(dummyG, group_by, sort_by):
    """Test for arc layout.

    Checks:

    1. X-axis minimum is 0.
    2. X-axis maximum is 2 * (num_nodes - 1)
    3. Y-axis remains at 0 all the time.
    """

    pos, nt = get_pos_df(dummyG, layouts.arc, group_by=group_by, sort_by=sort_by)
    assert pos["x"].min() == 0
    assert pos["x"].max() == 2 * (len(nt) - 1)
    assert all(pos["y"] == 0.0)


@pytest.mark.usefixtures("dummyG")
@pytest.mark.parametrize("sort_by", ("value", None))
@pytest.mark.parametrize("group_by", ("group", None))
def test_matrix(dummyG, group_by, sort_by):
    """Test for matrix layout.

    Checks:

    1. X-axis minimum is at 1.0
    2. Y-axis minimum is at 1.0
    3. X-axis maximum is at num_nodes.
    4. Y-axis maximum is at num_nodes.
    """
    pos, nt = get_pos_df(dummyG, layouts.matrix, group_by=group_by, sort_by=sort_by)

    assert pos["x"].min() == 2.0
    assert pos["y"].min() == 0.0
    assert pos["x"].max() == 2 * len(nt)
    assert pos["y"].max() == 0.0

    pos, nt = get_pos_df(
        dummyG, layouts.matrix, group_by=group_by, sort_by=sort_by, axis="y"
    )

    assert pos["x"].min() == 0.0
    assert pos["y"].min() == 2.0
    assert pos["x"].max() == 0.0
    assert pos["y"].max() == 2 * len(nt)


@pytest.mark.usefixtures("dummyG")
def test_geo(geoG, group_by=None, sort_by=None):
    """Test for geo layout.

    Checks: None. This is just an execution test.
    """
    pos, nt = get_pos_df(geoG, layouts.geo, group_by=group_by, sort_by=sort_by)


@pytest.mark.usefixtures("dummyG")
@pytest.mark.parametrize("sort_by", ("value", None))
def test_hive(dummyG, sort_by):
    """Hive plot node layout execution test."""
    pos, nt = get_pos_df(dummyG, layouts.hive, group_by="group", sort_by=sort_by)


@pytest.mark.usefixtures("manygroupG")
@pytest.mark.parametrize("sort_by", ("value", None))
def test_hive_manygroups(manygroupG, sort_by):
    """Test that hive layout raises an error when there are too many groups."""
    with pytest.raises(ValueError):
        pos, nt = get_pos_df(
            manygroupG, layouts.hive, group_by="group", sort_by=sort_by
        )
