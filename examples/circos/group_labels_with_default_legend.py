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
    node_label_rotation=True,
    node_label_color=True,
    group_label_color=True,
    node_label_layout='numbers',
    group_order='alphabetically',
    fontsize=10,
    group_legend=True,
    figsize=(12, 12)
)

# Draw the CircosPlot
c.draw()
c.figure.tight_layout()

# Save figure
plt.savefig(
    'circusplot_defaultlegend.png',
    format='png',
    dpi=400,
    bbox_inches="tight")

# Display graph
plt.show()
