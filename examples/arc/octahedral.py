"""
Displays a NetworkX octahedral graph to screen using a ArcPlot.
"""

import matplotlib.pyplot as plt
import networkx as nx

from nxviz.plots import ArcPlot

G = nx.octahedral_graph()
c = ArcPlot(G)
c.draw()
plt.show()
