import matplotlib.pyplot as plt
import networkx as nx
from random import randint

import nxviz as nv

G = nx.erdos_renyi_graph(n=30, p=0.1, directed=True)
for n, d in G.nodes(data=True):
    G.nodes[n]["group"] = randint(0, 30)

for u, v, d in G.edges(data=True):
    d["weight"] = randint(0, 10)

nv.circos(
    G,
    group_by="group",
    node_color_by="group",
    edge_color_by="source_node_color",
    edge_alpha_by="weight",
)

plt.show()
