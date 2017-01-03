"""
Displays a NetworkX octahedral graph to screen using a CircosPlot.
"""

from nxviz.plots import CircosPlot
import networkx as nx
import matplotlib.pyplot as plt

G = nx.octahedral_graph()
c = CircosPlot(G)
c.draw()
plt.show()
