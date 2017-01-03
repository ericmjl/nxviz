"""
Displays a NetworkX barbell graph to screen using a CircosPlot.
"""

from nxviz.plots import CircosPlot
import networkx as nx
import matplotlib.pyplot as plt

G = nx.barbell_graph(m1=10, m2=3)
c = CircosPlot(G)
c.draw()
plt.show()
