from random import choice

import matplotlib.pyplot as plt
import networkx as nx

from nxviz.plots import CircosPlot

G = nx.barbell_graph(m1=10, m2=3)
for n, d in G.nodes(data=True):
    G.node[n]["class"] = choice(["a", "b", "c", "d", "e"])
c = CircosPlot(
    G,
    node_grouping="class",
    node_color="class",
    node_order="class",
    node_labels=True,
    group_label_position="middle",
    group_label_color=True,
    group_label_offset=2,
)
c.draw()
plt.show()
