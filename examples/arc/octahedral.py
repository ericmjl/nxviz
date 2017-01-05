"""
Displays a NetworkX octahedral graph to screen using a ArcPlot.
"""

from nxviz.plots import ArcPlot
import networkx as nx
import matplotlib.pyplot as plt

G = nx.octahedral_graph()
c = ArcPlot(G)
c.draw()
plt.show()
