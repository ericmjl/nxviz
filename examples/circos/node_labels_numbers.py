# Author: Alireza Hosseini
from random import randint

import matplotlib.pyplot as plt
import networkx as nx

import nxviz as nv
from nxviz import annotate

G = nx.erdos_renyi_graph(n=30, p=0.1)
for n, d in G.nodes(data=True):
    G.nodes[n]["group"] = randint(0, 5)
G = nx.relabel_nodes(G, {i: "long name #" + str(i) for i in range(len(G))})

nv.circos(G, group_by="group", node_color_by="group")
annotate.circos_labels(G, group_by="group", layout="numbers")
# The numbered labels take up more space, so we will have to increase the
# padding a bit. 15% on all sides works well here.
plt.tight_layout(rect=(0.15, 0.15, 0.85, 0.85))
plt.show()
