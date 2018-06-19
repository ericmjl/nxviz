"""
Displays a NetworkX lollipop graph to screen using a CircosPlot.
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy.random as npr

from nxviz.plots import CircosPlot

G = nx.lollipop_graph(m=10, n=4)
for n, d in G.nodes(data=True):
    G.node[n]["value"] = npr.normal()
c = CircosPlot(G, node_color="value", node_order="value")
c.draw()
plt.show()
