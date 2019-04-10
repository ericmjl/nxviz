"""
Displays different edge_colors with ArcPlot
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


G.add_edge("A", "B", weight=5, type="a")
G.add_edge("A", "C", weight=5, type="b")
G.add_edge("B", "C", weight=5, type="a")
G.add_edge("C", "B", weight=5, type="b")


edges = G.edges()

c = ArcPlot(
    G,
    node_labels=True,
    node_size="n_visitors",
    node_color="n_visitors",
    edge_width="weight",
    edge_color="type"
)

c.draw()
plt.show()
