"""Tests for nxviz.paths module — backend-agnostic edge path coordinate computation."""

import numpy as np
import pytest

from nxviz import paths
from nxviz.utils import edge_table, node_table

from .fixtures.graphs import make_dummyG


@pytest.fixture
def dummy_graph():
    return make_dummyG()


@pytest.fixture
def graph_tables(dummy_graph):
    nt = node_table(dummy_graph)
    et = edge_table(dummy_graph)
    return nt, et


class TestCircosCoords:
    def test_returns_list_of_arrays(self, dummy_graph, graph_tables):
        from nxviz.layouts import circos

        nt, et = graph_tables
        pos = circos(nt, group_by="group", sort_by="value")
        coords = paths.circos_coords(et, pos)
        assert isinstance(coords, list)
        assert len(coords) == len(et)

    def test_each_array_shape_3_2(self, dummy_graph, graph_tables):
        from nxviz.layouts import circos

        nt, et = graph_tables
        pos = circos(nt, group_by="group", sort_by="value")
        coords = paths.circos_coords(et, pos)
        for arr in coords:
            assert arr.shape == (3, 2)

    def test_middle_point_is_origin(self, dummy_graph, graph_tables):
        from nxviz.layouts import circos

        nt, et = graph_tables
        pos = circos(nt, group_by="group", sort_by="value")
        coords = paths.circos_coords(et, pos)
        for arr in coords:
            np.testing.assert_allclose(arr[1], [0.0, 0.0])


class TestLineCoords:
    def test_returns_list_of_arrays(self, dummy_graph, graph_tables):
        from nxviz.layouts import arc

        nt, et = graph_tables
        pos = arc(nt, group_by="group", sort_by="value")
        coords = paths.line_coords(et, pos)
        assert isinstance(coords, list)
        assert len(coords) == len(et)

    def test_each_array_shape_2_2(self, dummy_graph, graph_tables):
        from nxviz.layouts import arc

        nt, et = graph_tables
        pos = arc(nt, group_by="group", sort_by="value")
        coords = paths.line_coords(et, pos)
        for arr in coords:
            assert arr.shape == (2, 2)


class TestArcCoords:
    def test_returns_list_of_arrays(self, dummy_graph, graph_tables):
        from nxviz.layouts import arc

        nt, et = graph_tables
        pos = arc(nt, group_by="group", sort_by="value")
        coords = paths.arc_coords(et, pos)
        assert isinstance(coords, list)
        assert len(coords) == len(et)

    def test_each_array_has_n_points(self, dummy_graph, graph_tables):
        from nxviz.layouts import arc

        nt, et = graph_tables
        pos = arc(nt, group_by="group", sort_by="value")
        coords = paths.arc_coords(et, pos, n_points=30)
        for arr in coords:
            assert arr.shape == (30, 2)


class TestHiveCoords:
    def test_returns_list_of_arrays_curves(self, dummy_graph, graph_tables):
        from nxviz.layouts import hive

        nt, et = graph_tables
        pos = hive(nt, group_by="group", sort_by="value")
        pos_cloned = hive(nt, group_by="group", sort_by="value", rotation=np.pi / 6)
        coords = paths.hive_coords(et, pos, pos_cloned, curves=True)
        assert isinstance(coords, list)
        assert len(coords) == len(et)

    def test_curves_true_shape_4_2(self, dummy_graph, graph_tables):
        from nxviz.layouts import hive

        nt, et = graph_tables
        pos = hive(nt, group_by="group", sort_by="value")
        pos_cloned = hive(nt, group_by="group", sort_by="value", rotation=np.pi / 6)
        coords = paths.hive_coords(et, pos, pos_cloned, curves=True)
        for arr in coords:
            assert arr.shape == (4, 2) or arr.shape == (2, 2)

    def test_curves_false_shape_2_2(self, dummy_graph, graph_tables):
        from nxviz.layouts import hive

        nt, et = graph_tables
        pos = hive(nt, group_by="group", sort_by="value")
        pos_cloned = hive(nt, group_by="group", sort_by="value", rotation=np.pi / 6)
        coords = paths.hive_coords(et, pos, pos_cloned, curves=False)
        for arr in coords:
            assert arr.shape == (2, 2)

    def test_no_pos_cloned_defaults_to_pos(self, dummy_graph, graph_tables):
        from nxviz.layouts import hive

        nt, et = graph_tables
        pos = hive(nt, group_by="group", sort_by="value")
        coords = paths.hive_coords(et, pos, pos_cloned=None, curves=False)
        assert isinstance(coords, list)
        assert len(coords) == len(et)


class TestMatrixCoords:
    def test_returns_list_of_tuples(self, dummy_graph, graph_tables):
        from nxviz.layouts import matrix

        nt, et = graph_tables
        pos = matrix(nt, group_by="group", sort_by="value", axis="x")
        pos_cloned = matrix(nt, group_by="group", sort_by="value", axis="y")
        coords = paths.matrix_coords(et, pos, pos_cloned)
        assert isinstance(coords, list)
        assert len(coords) == len(et)

    def test_each_element_is_2_element_tuple(self, dummy_graph, graph_tables):
        from nxviz.layouts import matrix

        nt, et = graph_tables
        pos = matrix(nt, group_by="group", sort_by="value", axis="x")
        pos_cloned = matrix(nt, group_by="group", sort_by="value", axis="y")
        coords = paths.matrix_coords(et, pos, pos_cloned)
        for coord in coords:
            assert len(coord) == 2
            assert isinstance(float(coord[0]), float)
            assert isinstance(float(coord[1]), float)
