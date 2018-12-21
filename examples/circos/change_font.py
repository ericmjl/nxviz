"""
Shows how to rotate node labels. This increaes legibility for longer labels.
"""

from random import choice
import matplotlib.pyplot as plt
import networkx as nx
from nxviz import CircosPlot

G = nx.barbell_graph(m1=20, m2=3)
for n, d in G.nodes(data=True):
    G.node[n]["class"] = choice(["one", "two", "three", "four", "five"])

c = CircosPlot(
    G,
    node_grouping="class",
    node_color="class",
    node_order="class",
    group_label_position="middle",
    nodeprops={"radius": 1},
    node_label_layout="rotation",
    fontsize=12,
    fontfamily="fantasy",
)
c.draw()
plt.show()
