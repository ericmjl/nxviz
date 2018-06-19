"""
Shows how to rotate node labels. This increaes legibility for longer labels.
"""

import matplotlib.pyplot as plt
import networkx as nx

from nxviz import CircosPlot

G = nx.barbell_graph(m1=20, m2=3)
# let's give the nodes some longer labels
G = nx.relabel_nodes(G, {i: "long name " + str(i) for i in range(len(G))})

# try it `node_label_layout=False` to see how the long names overlap each other
c = CircosPlot(G, node_labels=True, node_label_layout="rotation")
c.draw()
# the rotated labels take up more space, so we will have to increase the
# padding a bit. 15% on all sides works well here.
plt.tight_layout(rect=(0.15, 0.15, 0.85, 0.85))
plt.show()
