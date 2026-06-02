"""Tests for the Plotly backend — interactive web-based network visualizations."""

import numpy as np
import pandas as pd
import pytest

import nxviz as nv
from nxviz.backend import get_backend
from nxviz.utils import edge_table, node_table

from .fixtures.graphs import make_dummyG

try:
    import plotly.graph_objects as go

    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

pytestmark = pytest.mark.skipif(not HAS_PLOTLY, reason="plotly not installed")


@pytest.fixture
def dummyG():
    return make_dummyG()


@pytest.fixture
def plotly_backend():
    return get_backend("plotly")


class TestPlotlyBackendBasic:
    def test_create_axes_returns_figure(self, plotly_backend):
        fig = plotly_backend.create_axes()
        assert isinstance(fig, go.Figure)

    def test_get_figure_returns_figure(self, plotly_backend):
        fig = plotly_backend.create_axes()
        result = plotly_backend.get_figure(fig)
        assert result is fig

    def test_despine(self, plotly_backend):
        fig = plotly_backend.create_axes()
        plotly_backend.despine(fig)
        xaxis = fig.layout.xaxis
        yaxis = fig.layout.yaxis
        assert xaxis.showline is False
        assert yaxis.showline is False

    def test_set_aspect_equal(self, plotly_backend):
        fig = plotly_backend.create_axes()
        plotly_backend.set_aspect_equal(fig)
        assert fig.layout.yaxis.scaleanchor == "x"

    def test_rescale(self, plotly_backend):
        fig = plotly_backend.create_axes()
        pos = {0: np.array([1.0, 2.0]), 1: np.array([3.0, 4.0])}
        plotly_backend.rescale(fig, pos)
        assert fig.layout.xaxis.range is not None
        assert fig.layout.yaxis.range is not None


class TestPlotlyBackendDrawNodes:
    def test_draw_nodes_adds_scatter_trace(self, plotly_backend, dummyG):
        fig = plotly_backend.create_axes()
        nt = node_table(dummyG)
        from nxviz.layouts import circos
        from nxviz.nodes import node_colors, node_size, transparency

        pos = circos(nt, group_by="group", sort_by="value")
        colors = node_colors(nt, "group")
        alphas = transparency(nt, None)
        sizes = node_size(nt, None)

        plotly_backend.draw_nodes(fig, nt, pos, colors, alphas, sizes)
        assert len(fig.data) == 1
        assert isinstance(fig.data[0], go.Scatter)
        assert fig.data[0].mode == "markers"

    def test_draw_nodes_correct_count(self, plotly_backend, dummyG):
        fig = plotly_backend.create_axes()
        nt = node_table(dummyG)
        from nxviz.layouts import circos
        from nxviz.nodes import node_colors, node_size, transparency

        pos = circos(nt, group_by="group", sort_by="value")
        colors = node_colors(nt, "group")
        alphas = transparency(nt, None)
        sizes = node_size(nt, None)

        plotly_backend.draw_nodes(fig, nt, pos, colors, alphas, sizes)
        assert len(fig.data[0].x) == len(nt)

    def test_draw_nodes_has_hover_text(self, plotly_backend, dummyG):
        fig = plotly_backend.create_axes()
        nt = node_table(dummyG)
        from nxviz.layouts import circos
        from nxviz.nodes import node_colors, node_size, transparency

        pos = circos(nt, group_by="group", sort_by="value")
        colors = node_colors(nt, "group")
        alphas = transparency(nt, None)
        sizes = node_size(nt, None)

        plotly_backend.draw_nodes(fig, nt, pos, colors, alphas, sizes)
        assert fig.data[0].text is not None
        assert len(fig.data[0].text) == len(nt)


class TestPlotlyBackendDrawEdges:
    def test_draw_circos_edges(self, plotly_backend, dummyG):
        from nxviz import paths as nxviz_paths
        from nxviz.layouts import circos

        fig = plotly_backend.create_axes()
        nt = node_table(dummyG)
        et = edge_table(dummyG)
        pos = circos(nt, group_by="group", sort_by="value")
        path_coords = nxviz_paths.circos_coords(et, pos)
        colors = pd.Series(["black"] * len(et))
        alphas = pd.Series([0.1] * len(et))
        lw = pd.Series([1.0] * len(et))

        plotly_backend.draw_edges(
            fig, et, pos, path_coords, colors, alphas, lw, "circos"
        )
        edge_traces = [t for t in fig.data if getattr(t, "name", None) == "edges"]
        assert len(edge_traces) > 0

    def test_draw_line_edges(self, plotly_backend, dummyG):
        from nxviz import paths as nxviz_paths
        from nxviz.layouts import arc

        fig = plotly_backend.create_axes()
        nt = node_table(dummyG)
        et = edge_table(dummyG)
        pos = arc(nt, group_by="group", sort_by="value")
        path_coords = nxviz_paths.line_coords(et, pos)
        colors = pd.Series(["black"] * len(et))
        alphas = pd.Series([0.1] * len(et))
        lw = pd.Series([1.0] * len(et))

        plotly_backend.draw_edges(fig, et, pos, path_coords, colors, alphas, lw, "line")
        edge_traces = [t for t in fig.data if getattr(t, "name", None) == "edges"]
        assert len(edge_traces) > 0

    def test_draw_matrix_edges(self, plotly_backend, dummyG):
        from nxviz import paths as nxviz_paths
        from nxviz.layouts import matrix

        fig = plotly_backend.create_axes()
        nt = node_table(dummyG)
        et = edge_table(dummyG)
        pos = matrix(nt, group_by="group", sort_by="value", axis="x")
        pos_cloned = matrix(nt, group_by="group", sort_by="value", axis="y")
        path_coords = nxviz_paths.matrix_coords(et, pos, pos_cloned)
        colors = pd.Series(["black"] * len(et))
        alphas = pd.Series([0.1] * len(et))
        lw = pd.Series([1.0] * len(et))

        plotly_backend.draw_edges(
            fig,
            et,
            pos,
            path_coords,
            colors,
            alphas,
            lw,
            "matrix",
            pos_cloned=pos_cloned,
        )
        edge_traces = [t for t in fig.data if getattr(t, "name", None) == "edges"]
        assert len(edge_traces) > 0
        assert edge_traces[0].mode == "markers"

    def test_draw_hive_edges(self, plotly_backend, dummyG):
        from nxviz import paths as nxviz_paths
        from nxviz.layouts import hive

        fig = plotly_backend.create_axes()
        nt = node_table(dummyG)
        et = edge_table(dummyG)
        pos = hive(nt, group_by="group", sort_by="value")
        pos_cloned = hive(nt, group_by="group", sort_by="value", rotation=np.pi / 6)
        path_coords = nxviz_paths.hive_coords(et, pos, pos_cloned)
        colors = pd.Series(["black"] * len(et))
        alphas = pd.Series([0.1] * len(et))
        lw = pd.Series([1.0] * len(et))

        plotly_backend.draw_edges(
            fig,
            et,
            pos,
            path_coords,
            colors,
            alphas,
            lw,
            "hive",
            pos_cloned=pos_cloned,
        )
        edge_traces = [t for t in fig.data if getattr(t, "name", None) == "edges"]
        assert len(edge_traces) > 0


class TestPlotlyHighLevelAPI:
    """Test that high-level API functions work with backend='plotly'."""

    def test_circos_returns_figure(self, dummyG):
        fig = nv.circos(
            dummyG,
            group_by="group",
            sort_by="value",
            node_color_by="group",
            backend="plotly",
        )
        assert isinstance(fig, go.Figure)

    def test_arc_returns_figure(self, dummyG):
        fig = nv.arc(
            dummyG,
            group_by="group",
            sort_by="value",
            node_color_by="group",
            backend="plotly",
        )
        assert isinstance(fig, go.Figure)

    def test_parallel_returns_figure(self, dummyG):
        fig = nv.parallel(
            dummyG,
            group_by="group",
            sort_by="value",
            node_color_by="group",
            backend="plotly",
        )
        assert isinstance(fig, go.Figure)

    def test_hive_returns_figure(self, dummyG):
        fig = nv.hive(
            dummyG,
            group_by="group",
            sort_by="value",
            node_color_by="group",
            backend="plotly",
        )
        assert isinstance(fig, go.Figure)

    def test_matrix_returns_figure(self, dummyG):
        fig = nv.matrix(
            dummyG,
            group_by="group",
            sort_by="value",
            node_color_by="group",
            backend="plotly",
        )
        assert isinstance(fig, go.Figure)

    def test_circos_with_encodings(self, dummyG):
        fig = nv.circos(
            dummyG,
            group_by="group",
            sort_by="value",
            node_color_by="group",
            node_alpha_by="value",
            edge_alpha_by="edge_value",
            backend="plotly",
        )
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 2

    def test_circos_has_node_and_edge_traces(self, dummyG):
        fig = nv.circos(
            dummyG,
            group_by="group",
            sort_by="value",
            backend="plotly",
        )
        names = [getattr(t, "name", None) for t in fig.data]
        assert "nodes" in names
        assert "edges" in names

    def test_default_backend_is_matplotlib(self, dummyG):
        from matplotlib import pyplot as plt

        fig, ax = plt.subplots()
        result = nv.circos(
            dummyG,
            group_by="group",
            sort_by="value",
        )
        from matplotlib.axes import Axes

        assert isinstance(result, Axes)
        plt.close(fig)

    def test_geo_returns_figure(self, dummyG):
        for n in dummyG.nodes():
            dummyG.nodes[n]["longitude"] = np.random.normal()
            dummyG.nodes[n]["latitude"] = np.random.normal()
        fig = nv.geo(dummyG, backend="plotly")
        assert isinstance(fig, go.Figure)

    def test_circos_edge_color_by(self, dummyG):
        fig = nv.circos(
            dummyG,
            group_by="group",
            sort_by="value",
            edge_color_by="edge_value",
            backend="plotly",
        )
        assert isinstance(fig, go.Figure)
