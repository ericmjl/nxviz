"""
Displays different node_size with ArcPlot
"""

import matplotlib.pyplot as plt
import networkx as nx
from nxviz.plots import ArcPlot

G = nx.Graph()

G.add_node("A", score=1.5)
G.add_node("B", score=0.5)
G.add_node("C", score=1)


G.add_edge("A", "B", weight=8, type="a")
G.add_edge("A", "C", weight=8, type="b")
G.add_edge("B", "C", weight=8, type="a")


c = ArcPlot(G, node_size="score", edge_width="weight", edge_color="type")

c.draw()
plt.show()
