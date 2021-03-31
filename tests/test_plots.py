"""
Some rudimentary tests. Instantiates a Plot object, but doesn't test plotting.

Discovered that this set of rudimentary tests might be necessary after seeing
the following issue:

    https://github.com/ericmjl/nxviz/issues/160
"""

# from test_utils import diff_plots, corresponding_lists

from random import random
from matplotlib import pyplot as plt

import networkx as nx


# from nxviz import ArcPlot, CircosPlot, GeoPlot, MatrixPlot
from nxviz.plots import despine, respine, rescale, rescale_arc, rescale_square

# from matplotlib.testing.decorators import _image_directories

# G = nx.erdos_renyi_graph(n=20, p=0.2)

# G_geo = G.copy()
# for n, d in G_geo.nodes(data=True):
#     G_geo.nodes[n]["latitude"] = random()
#     G_geo.nodes[n]["longitude"] = random()
#     G_geo.nodes[n]["dpcapacity"] = random()

# baseline_dir, result_dir = _image_directories(lambda: "dummy func")


def test_despine():
    """Test that despine removes all spines from matplotlib axes."""
    despine()
    ax = plt.gca()

    assert not ax.xaxis.get_visible()
    assert not ax.yaxis.get_visible()

    for spine in ax.spines:
        assert not ax.spines[spine].get_visible()


def test_respine():
    """Test that respine reinstates all spines from matplotlib axes."""
    despine()
    respine()
    ax = plt.gca()

    assert ax.xaxis.get_visible()
    assert ax.yaxis.get_visible()

    for spine in ax.spines:
        assert ax.spines[spine].get_visible()


# def test_circos_plot():
#     c = CircosPlot(G)  # noqa: F841
#     diff = diff_plots(c, "circos.png", baseline_dir, result_dir)
#     assert diff is None


# def test_matrix_plot():
#     m = MatrixPlot(G)  # noqa: F841
#     diff = diff_plots(m, "matrix.png", baseline_dir, result_dir)
#     assert diff is None


# def test_arc_plot():
#     a = ArcPlot(G)  # noqa: F841
#     diff = diff_plots(a, "arc.png", baseline_dir, result_dir)
#     assert diff is None


# def test_geo_plot():
#     g = GeoPlot(
#         G_geo,
#         node_lat="latitude",
#         node_lon="longitude",  # noqa: F841
#         color="dpcapacity",
#     )
#     diff = diff_plots(g, "geo.png", baseline_dir, result_dir)
#     assert diff is None


# def test_plot_size():
#     c = CircosPlot(G, figsize=(3, 3))  # noqa: F841
#     diff = diff_plots(c, "circos33.png", baseline_dir, result_dir)
#     assert diff is None


# def test_edge_widths():
#     # add weight as attribute and fill with random numbers
#     edges = G.edges()
#     for u, v in edges:
#         G[u][v]["weight"] = random()
#     # also extract list for testing
#     weights = [G[u][v]["weight"] for u, v in edges]
#     # add weights as property
#     c = CircosPlot(G, edge_width="weight")
#     assert c.edge_widths == weights
#     a = ArcPlot(G, edge_width="weight")
#     assert a.edge_widths == weights
#     # add weights as list
#     c = CircosPlot(G, edge_width=weights)
#     assert c.edge_widths == weights
#     a = ArcPlot(G, edge_width=weights)
#     assert a.edge_widths == weights


# def test_edge_color():
#     # add color as attribute and fill with random numbers
#     edges = G.edges()
#     for u, v in edges:
#         G[u][v]["type"] = "a" if random() < 0.5 else "b"
#     # also extract list for testing
#     types = [G[u][v]["type"] for u, v in edges]
#     # add color as property
#     c = CircosPlot(G, edge_color="type")
#     assert corresponding_lists(c.edge_colors, types)
#     a = ArcPlot(G, edge_color="type")
#     assert corresponding_lists(a.edge_colors, types)


# def test_node_size():
#     # add size as attribute and fill with random numbers
#     nodes = G.nodes()
#     for u in nodes:
#         G.nodes[u]["score"] = random()
#     # also extract list for testing
#     scores = [G.nodes[u]["score"] for u in nodes]
#     # add color as property
#     a = ArcPlot(G, node_size="score")
#     assert a.node_sizes == scores
#     # add types as list
#     a = ArcPlot(G, node_size=scores)
#     assert a.node_sizes == scores
