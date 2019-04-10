"""
Displays different edge_colors with ArcPlot
"""

import matplotlib.pyplot as plt
import networkx as nx
from nxviz.plots import ArcPlot

G = nx.DiGraph()

G.add_node("A")
G.add_node("B")
G.add_node("C")


G.add_edge("A", "B", weight=8, type="a")
G.add_edge("A", "C", weight=8, type="b")
G.add_edge("B", "C", weight=8, type="a")


edges = G.edges()

c = ArcPlot(
    G,
    edge_width="weight",
    edge_color="type"
)

c.draw()
plt.show()
