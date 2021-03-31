"""Tests for annotation."""

import pytest
import nxviz as nv
from nxviz import annotate


@pytest.mark.usefixtures("dummyG")
def test_circos_group(dummyG):
    """Execution test for circos group annotations."""
    ax = nv.circos(dummyG, group_by="group")
    annotate.circos_group(dummyG, group_by="group")


@pytest.mark.usefixtures("dummyG")
def test_hive_group(dummyG):
    """Execution test for hive group annotations."""
    ax = nv.hive(dummyG, group_by="group")
    annotate.hive_group(dummyG, group_by="group")


@pytest.mark.usefixtures("dummyG")
def test_arc_group(dummyG):
    """Execution test for arc group annotations."""
    ax = nv.arc(dummyG, group_by="group")
    annotate.arc_group(dummyG, group_by="group")


@pytest.mark.usefixtures("dummyG")
def test_parallel_group(dummyG):
    """Execution test for parallel coordinates' group annotations."""
    ax = nv.parallel(dummyG, group_by="group")
    annotate.parallel_group(dummyG, group_by="group")


@pytest.mark.usefixtures("dummyG")
def test_matrix_group(dummyG):
    """Execution test for matrix group annotations."""
    ax = nv.matrix(dummyG, group_by="group")
    annotate.matrix_group(dummyG, group_by="group")


@pytest.mark.usefixtures("dummyG")
def test_matrix_block(dummyG):
    """Execution test for matrix block annotations."""
    ax = nv.matrix(dummyG, group_by="group", node_color_by="group")
    annotate.matrix_block(dummyG, group_by="group", color_by="group")


@pytest.mark.usefixtures("dummyG")
def test_node_colormapping(dummyG):
    """Execution test for node_colormapping."""
    ax = nv.circos(dummyG, group_by="group", node_color_by="group")
    annotate.node_colormapping(dummyG, color_by="group")


@pytest.mark.usefixtures("dummyG")
def test_edge_colormapping(dummyG):
    """Execution test for edge_colormapping."""
    ax = nv.circos(dummyG, group_by="group", edge_color_by="edge_value")
    annotate.edge_colormapping(dummyG, color_by="edge_value")


@pytest.mark.usefixtures("smallG")
def test_node_labels(smallG):
    """Execution test for node labels."""
    ax = nv.arc(smallG)
    annotate.arc_labels(smallG)
