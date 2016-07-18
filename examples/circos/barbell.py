"""
Displays a NetworkX octahedral graph to screen using a CircosPlot.
"""

from nxviz.circos import CircosPlot
import networkx as nx
import matplotlib.pyplot as plt

G = nx.barbell_graph(m1=10, m2=3)
c = CircosPlot(G.nodes(), G.edges(), radius=5)
c.draw()
plt.show()
