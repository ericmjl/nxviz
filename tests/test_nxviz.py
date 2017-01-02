from nxviz.plots import BasePlot
import networkx as nx


def test_initialization():
    """
    Tests initialization of plot object.
    """
    n_nodes = 10
    G = nx.erdos_renyi_graph(n=n_nodes, p=0.3)

    b = BasePlot(graph=G)

    assert len(b.nodes) == len(G.nodes())
