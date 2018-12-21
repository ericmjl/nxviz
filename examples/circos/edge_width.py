"""
Shows different edge widths on CircusPlot
"""
import matplotlib.pyplot as plt
import networkx as nx
from nxviz.plots import CircosPlot

nodelist = [("a"), ("b"), ("c"), ("d"), ("e"), ("f")]
edgelist1 = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "f")]

weights = list(range(6))

G = nx.Graph()
G.add_nodes_from(nodelist)
G.add_edges_from(edgelist1)
c = CircosPlot(graph=G, edge_width=weights)
c.draw()

plt.show()
