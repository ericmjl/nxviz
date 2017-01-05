"""
Displays a NetworkX octahedral graph to screen using a MatrixPlot.
"""

from nxviz.plots import MatrixPlot
import networkx as nx
import matplotlib.pyplot as plt

G = nx.octahedral_graph()
c = MatrixPlot(G)
c.draw()
plt.show()
