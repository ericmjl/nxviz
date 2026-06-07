"""Tests for chord diagram compute-phase functions and API."""

import matplotlib

matplotlib.use("Agg")

import numpy as np
import pandas as pd
import pytest

from nxviz.chord_compute import aggregate_edges, group_arcs, ribbon_coords
from nxviz.utils import edge_table, node_table

from .fixtures.graphs import make_dummyG


def make_chord_graph():
    """Build a directed graph with continent grouping and flow weights."""
    import networkx as nx

    G = nx.DiGraph()
    continents = {
        "Nigeria": "Africa",
        "Egypt": "Africa",
        "South Africa": "Africa",
        "China": "Asia",
        "India": "Asia",
        "Japan": "Asia",
        "Germany": "Europe",
        "France": "Europe",
        "UK": "Europe",
        "USA": "N. America",
        "Canada": "N. America",
        "Mexico": "N. America",
        "Brazil": "S. America",
        "Argentina": "S. America",
        "Australia": "Oceania",
        "New Zealand": "Oceania",
    }
    for country, continent in continents.items():
        G.add_node(country, continent=continent)
    flows = [
        ("India", "UK", 500000),
        ("India", "USA", 800000),
        ("Mexico", "USA", 1200000),
        ("China", "USA", 400000),
        ("Nigeria", "UK", 300000),
        ("France", "UK", 200000),
        ("Brazil", "USA", 300000),
        ("UK", "Australia", 250000),
        ("Germany", "USA", 200000),
        ("Egypt", "France", 150000),
        ("South Africa", "UK", 200000),
        ("China", "Australia", 350000),
        ("India", "Canada", 250000),
    ]
    for src, tgt, flow in flows:
        G.add_edge(src, tgt, flow=flow)
    return G


@pytest.fixture
def chord_graph():
    return make_chord_graph()


class TestGroupArcs:
    def test_returns_dataframe(self, chord_graph):
        nt = node_table(chord_graph)
        result = group_arcs(nt, "continent")
        assert isinstance(result, pd.DataFrame)

    def test_columns(self, chord_graph):
        nt = node_table(chord_graph)
        result = group_arcs(nt, "continent")
        expected_cols = {"group", "start_angle", "end_angle", "n_nodes", "color"}
        assert set(result.columns) == expected_cols

    def test_one_row_per_group(self, chord_graph):
        nt = node_table(chord_graph)
        result = group_arcs(nt, "continent")
        n_groups = nt["continent"].nunique()
        assert len(result) == n_groups

    def test_angular_extents_sum_to_2pi_minus_gaps(self, chord_graph):
        nt = node_table(chord_graph)
        gap_fraction = 0.01
        result = group_arcs(nt, "continent", gap_fraction=gap_fraction)
        total_extent = (result["end_angle"] - result["start_angle"]).sum()
        n_groups = len(result)
        expected = 2 * np.pi - n_groups * 2 * np.pi * gap_fraction
        np.testing.assert_allclose(total_extent, expected, rtol=1e-10)

    def test_extents_proportional_to_node_count(self, chord_graph):
        nt = node_table(chord_graph)
        result = group_arcs(nt, "continent")
        total = result["n_nodes"].sum()
        extents = result["end_angle"] - result["start_angle"]
        proportions = extents / extents.sum()
        expected_proportions = result["n_nodes"] / total
        np.testing.assert_allclose(proportions.values, expected_proportions.values, rtol=1e-10)

    def test_single_group_raises(self):
        import networkx as nx

        G = nx.Graph()
        for i in range(5):
            G.add_node(i, group="A")
        nt = node_table(G)
        with pytest.raises(ValueError, match="at least 2 groups"):
            group_arcs(nt, "group")

    def test_colors_assigned(self, chord_graph):
        nt = node_table(chord_graph)
        result = group_arcs(nt, "continent")
        assert all(isinstance(c, tuple) and len(c) >= 3 for c in result["color"])

    def test_angles_monotonically_increasing(self, chord_graph):
        nt = node_table(chord_graph)
        result = group_arcs(nt, "continent")
        starts = result["start_angle"].values
        ends = result["end_angle"].values
        for i in range(len(result) - 1):
            assert ends[i] <= starts[i + 1]


class TestAggregateEdges:
    def test_returns_dataframe(self, chord_graph):
        nt = node_table(chord_graph)
        et = edge_table(chord_graph)
        result = aggregate_edges(et, nt, "continent")
        assert isinstance(result, pd.DataFrame)

    def test_columns(self, chord_graph):
        nt = node_table(chord_graph)
        et = edge_table(chord_graph)
        result = aggregate_edges(et, nt, "continent")
        assert set(result.columns) == {"source_group", "target_group", "weight"}

    def test_weight_by_sums(self, chord_graph):
        nt = node_table(chord_graph)
        et = edge_table(chord_graph)
        result = aggregate_edges(et, nt, "continent", weight_by="flow")
        asia_to_na = result[
            (result["source_group"] == "Asia")
            & (result["target_group"] == "N. America")
        ]
        assert len(asia_to_na) == 1
        assert asia_to_na["weight"].iloc[0] == 800000 + 400000 + 250000

    def test_no_weight_counts(self, chord_graph):
        nt = node_table(chord_graph)
        et = edge_table(chord_graph)
        result = aggregate_edges(et, nt, "continent")
        assert all(result["weight"] > 0)

    def test_missing_weight_raises(self, chord_graph):
        nt = node_table(chord_graph)
        et = edge_table(chord_graph)
        with pytest.raises(KeyError, match="not found"):
            aggregate_edges(et, nt, "continent", weight_by="nonexistent")

    def test_empty_edges_returns_empty(self, chord_graph):
        import networkx as nx

        G = nx.DiGraph()
        G.add_node("A", continent="X")
        G.add_node("B", continent="Y")
        nt = node_table(G)
        et = edge_table(G)
        result = aggregate_edges(et, nt, "continent")
        assert len(result) == 0
        assert set(result.columns) == {"source_group", "target_group", "weight"}


class TestRibbonCoords:
    def test_returns_list_of_dicts(self, chord_graph):
        nt = node_table(chord_graph)
        et = edge_table(chord_graph)
        arcs = group_arcs(nt, "continent")
        agg = aggregate_edges(et, nt, "continent", weight_by="flow")
        result = ribbon_coords(agg, arcs)
        assert isinstance(result, list)
        assert all(isinstance(r, dict) for r in result)

    def test_ribbon_keys(self, chord_graph):
        nt = node_table(chord_graph)
        et = edge_table(chord_graph)
        arcs = group_arcs(nt, "continent")
        agg = aggregate_edges(et, nt, "continent", weight_by="flow")
        result = ribbon_coords(agg, arcs)
        expected_keys = {
            "source_group",
            "target_group",
            "source_angle_start",
            "source_angle_end",
            "target_angle_start",
            "target_angle_end",
            "path_coords",
            "color",
            "alpha",
            "weight",
        }
        for ribbon in result:
            assert set(ribbon.keys()) == expected_keys

    def test_path_coords_are_arrays(self, chord_graph):
        nt = node_table(chord_graph)
        et = edge_table(chord_graph)
        arcs = group_arcs(nt, "continent")
        agg = aggregate_edges(et, nt, "continent", weight_by="flow")
        result = ribbon_coords(agg, arcs)
        for ribbon in result:
            assert isinstance(ribbon["path_coords"], np.ndarray)
            assert ribbon["path_coords"].shape[1] == 2

    def test_one_ribbon_per_aggregated_edge(self, chord_graph):
        nt = node_table(chord_graph)
        et = edge_table(chord_graph)
        arcs = group_arcs(nt, "continent")
        agg = aggregate_edges(et, nt, "continent", weight_by="flow")
        result = ribbon_coords(agg, arcs)
        assert len(result) == len(agg)

    def test_no_subband_overlaps_on_same_arc(self, chord_graph):
        nt = node_table(chord_graph)
        et = edge_table(chord_graph)
        arcs = group_arcs(nt, "continent")
        agg = aggregate_edges(et, nt, "continent", weight_by="flow")
        result = ribbon_coords(agg, arcs)

        from collections import defaultdict

        arc_bands = defaultdict(list)
        for r in result:
            sg, tg = r["source_group"], r["target_group"]
            arc_bands[sg].append(
                (r["source_angle_start"], r["source_angle_end"])
            )
            arc_bands[tg].append(
                (r["target_angle_start"], r["target_angle_end"])
            )

        for grp, bands in arc_bands.items():
            bands.sort()
            for i in range(len(bands) - 1):
                assert bands[i][1] <= bands[i + 1][0] + 1e-10, (
                    f"Overlap on {grp}: [{bands[i][0]:.4f},{bands[i][1]:.4f}] "
                    f"overlaps [{bands[i+1][0]:.4f},{bands[i+1][1]:.4f}]"
                )

    def test_subbands_within_arc_bounds(self, chord_graph):
        nt = node_table(chord_graph)
        et = edge_table(chord_graph)
        arcs = group_arcs(nt, "continent")
        agg = aggregate_edges(et, nt, "continent", weight_by="flow")
        result = ribbon_coords(agg, arcs)

        arc_bounds = {
            row["group"]: (row["start_angle"], row["end_angle"])
            for _, row in arcs.iterrows()
        }

        for r in result:
            sg, tg = r["source_group"], r["target_group"]
            src_start, src_end = arc_bounds[sg]
            tgt_start, tgt_end = arc_bounds[tg]
            assert r["source_angle_start"] >= src_start - 1e-10
            assert r["source_angle_end"] <= src_end + 1e-10
            assert r["target_angle_start"] >= tgt_start - 1e-10
            assert r["target_angle_end"] <= tgt_end + 1e-10

    def test_self_loop_subbands_sequential(self, chord_graph):
        nt = node_table(chord_graph)
        et = edge_table(chord_graph)
        arcs = group_arcs(nt, "continent")
        agg = aggregate_edges(et, nt, "continent", weight_by="flow")
        result = ribbon_coords(agg, arcs)

        for r in result:
            if r["source_group"] == r["target_group"]:
                assert r["source_angle_end"] <= r["target_angle_start"] + 1e-10, (
                    f"Self-loop on {r['source_group']}: source [{r['source_angle_start']:.4f},"
                    f"{r['source_angle_end']:.4f}] overlaps target "
                    f"[{r['target_angle_start']:.4f},{r['target_angle_end']:.4f}]"
                )


class TestChordAPI:
    def test_matplotlib_returns_axes(self, chord_graph):
        import matplotlib.pyplot as plt

        ax = plt.figure().add_subplot(111)
        import nxviz as nv

        result = nv.chord(chord_graph, group_by="continent", weight_by="flow")
        assert hasattr(result, "patches")

    def test_plotly_returns_figure(self, chord_graph):
        import nxviz as nv

        result = nv.chord(
            chord_graph, group_by="continent", weight_by="flow", backend="plotly"
        )
        import plotly.graph_objects as go

        assert isinstance(result, go.Figure)

    def test_group_by_none_raises(self, chord_graph):
        import nxviz as nv

        with pytest.raises(TypeError, match="group_by is required"):
            nv.chord(chord_graph, group_by=None)

    def test_undirected_graph(self):
        import networkx as nx

        import nxviz as nv

        G = nx.Graph()
        G.add_node("A", group="X")
        G.add_node("B", group="X")
        G.add_node("C", group="Y")
        G.add_node("D", group="Y")
        G.add_edge("A", "C")
        G.add_edge("B", "D")
        G.add_edge("A", "B")
        ax = nv.chord(G, group_by="group")
        assert hasattr(ax, "patches")

    def test_custom_alpha(self, chord_graph):
        import nxviz as nv

        result = nv.chord(
            chord_graph, group_by="continent", weight_by="flow", alpha=0.7
        )
        assert hasattr(result, "patches")
