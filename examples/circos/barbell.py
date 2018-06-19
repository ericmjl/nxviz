"""
Displays a NetworkX barbell graph to screen using a CircosPlot.
"""

from random import choice

import matplotlib.pyplot as plt
import networkx as nx

from nxviz.plots import CircosPlot

G = nx.barbell_graph(m1=10, m2=3)
for n, d in G.nodes(data=True):
    G.node[n]["class"] = choice(["one", "two", "three"])
c = CircosPlot(G, node_color="class", node_order="class", node_labels=True)
c.draw()
plt.show()
