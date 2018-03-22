"""
Displays a NetworkX octahedral graph to screen using a MatrixPlot.
"""

import matplotlib.pyplot as plt
import networkx as nx

from nxviz.plots import MatrixPlot

G = nx.octahedral_graph()
c = MatrixPlot(G)
c.draw()
plt.show()
