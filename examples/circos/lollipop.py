"""
Displays a NetworkX octahedral graph to screen using a CircosPlot.
"""

from nxviz.circos import CircosPlot
import networkx as nx
import matplotlib.pyplot as plt

G = nx.lollipop_graph(m=10, n=4)
c = CircosPlot(G.nodes(), G.edges(), radius=5)
c.draw()
plt.show()
