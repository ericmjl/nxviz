"""
Some rudimentary tests. Instantiates a Plot object, but doesn't test plotting.

Discovered that this set of rudimentary tests might be necessary after seeing
the following issue:

    https://github.com/ericmjl/nxviz/issues/160
"""

import networkx as nx

from nxviz import ArcPlot, CircosPlot, MatrixPlot

G = nx.erdos_renyi_graph(n=20, p=0.2)


def test_circos_plot():
    c = CircosPlot(G)


def test_matrix_plot():
    m = MatrixPlot(G)


def test_arc_plot():
    a = ArcPlot(G)


def test_plot_size():
    c = CircosPlot(G, figsize=(3, 3))
