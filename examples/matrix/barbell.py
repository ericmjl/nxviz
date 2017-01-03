"""
Displays a NetworkX barbell graph to screen using a CircosPlot.
"""

from nxviz.plots import MatrixPlot
import networkx as nx
import matplotlib.pyplot as plt

G = nx.barbell_graph(m1=10, m2=3)
c = MatrixPlot(G)
c.draw()
plt.show()
