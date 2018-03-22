"""
Displays a NetworkX octahedral graph to screen using a CircosPlot.
"""

import matplotlib.pyplot as plt
import networkx as nx

from nxviz.plots import CircosPlot

G = nx.octahedral_graph()
c = CircosPlot(G)
c.draw()
plt.show()
