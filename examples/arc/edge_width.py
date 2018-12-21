"""
Displays different edge_widths with ArcPlot, see also Issue #291
"""

import matplotlib.pyplot as plt
import networkx as nx
from nxviz.plots import ArcPlot

G = nx.DiGraph()

NODES_EBUNCH = [
    ("A", {"n_visitors": "1"}),
    ("B", {"n_visitors": "3"}),
    ("C", {"n_visitors": "4"}),
]

G.add_nodes_from(NODES_EBUNCH)

EDGES_EBUNCH = [("A", "B", 1), ("A", "C", 2), ("B", "C", 25), ("C", "B", 10)]

G.add_weighted_edges_from(EDGES_EBUNCH)

edges = G.edges()

c = ArcPlot(
    G,
    node_labels=True,
    node_size="n_visitors",
    node_color="n_visitors",
    edge_width="weight",
)

c.draw()
plt.show()
