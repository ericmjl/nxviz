"""
Shows different edge colors. Either categorial/ordinal or continuous
"""
import matplotlib.pyplot as plt
import networkx as nx
from nxviz.plots import CircosPlot

nodelist = [("a"), ("b"), ("c"), ("d"), ("e"), ("f")]
edgelist1 = [
    ("a", "b", {"weight": 0.1}),
    ("a", "c", {"weight": 0.2}),
    ("b", "d", {"weight": 0.6}),
    ("c", "d", {"weight": 0.7}),
    ("e", "d", {"weight": 0.8}),
    ("e", "f", {"weight": 1.0}),
]
edgelist2 = [
    ("a", "b", {"class": 1}),
    ("a", "c", {"class": 3}),
    ("b", "d", {"class": 8}),
    ("c", "d", {"class": 10}),
    ("e", "d", {"class": 5}),
    ("e", "f", {"class": 5}),
]

G = nx.Graph()
G.add_nodes_from(nodelist)
G.add_edges_from(edgelist1)
c = CircosPlot(graph=G, edge_color="weight")
c.draw()


F = nx.Graph()
F.add_nodes_from(nodelist)
F.add_edges_from(edgelist2)
d = CircosPlot(graph=F, edge_color="class")
d.draw()

plt.show()
