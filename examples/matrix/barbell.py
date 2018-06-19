"""
Displays a NetworkX barbell graph to screen using a CircosPlot.

Features of this example:
- MatrixPlot
- Styling matrix plot with different colormap.
"""

import matplotlib.pyplot as plt
import networkx as nx

from nxviz.plots import MatrixPlot

G = nx.barbell_graph(m1=10, m2=3)

# Instantiate a MatrixPlot with no custom styling.
m = MatrixPlot(G)

# Change the cmap prior to drawing.
m.cmap = plt.cm.get_cmap("Greens")
m.draw()
plt.show()
