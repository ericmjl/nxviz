# Author: Alireza Hosseini
from random import randint

import matplotlib.pyplot as plt
import networkx as nx

import nxviz as nv
from nxviz import annotate

G = nx.barbell_graph(m1=10, m2=3)
for n, d in G.nodes(data=True):
    G.nodes[n]["group"] = randint(0, 3)
G = nx.relabel_nodes(G, {i: "long name #" + str(i) for i in range(len(G))})

nv.arc(G, group_by="group", node_color_by="group")
annotate.arc_labels(G, group_by="group", layout="standard")
# The standard labels take up more space, so we will have to increase the
# padding a bit. 5% on all sides works well here.
plt.tight_layout(rect=(0.05, 0.05, 0.95, 0.95))
plt.show()
