"""
Some rudimentary tests. Instantiates a Plot object, but doesn't test plotting.

Discovered that this set of rudimentary tests might be necessary after seeing
the following issue:

    https://github.com/ericmjl/nxviz/issues/160
"""

import networkx as nx

from nxviz import ArcPlot, CircosPlot, GeoPlot, MatrixPlot

G = nx.erdos_renyi_graph(n=20, p=0.2)


def test_circos_plot():
    c = CircosPlot(G)  # noqa: F841


def test_matrix_plot():
    m = MatrixPlot(G)  # noqa: F841


def test_arc_plot():
    a = ArcPlot(G)  # noqa: F841


def test_geo_plot():
    G = nx.read_gpickle('data/divvy.pkl')  # noqa: N806
    g = GeoPlot(G, node_lat='latitude', node_lon='longitude',  # noqa: F841
                color='dpcapacity')


def test_plot_size():
    c = CircosPlot(G, figsize=(3, 3))  # noqa: F841
