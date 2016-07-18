"""
Displays a NetworkX octahedral graph to screen using a CircosPlot.
"""

from nxviz.circos import CircosPlot
import networkx as nx
import matplotlib.pyplot as plt

G = nx.octahedral_graph()
c = CircosPlot(G.nodes(), G.edges(), radius=5, node_radius=1)
c.draw()
plt.show()
