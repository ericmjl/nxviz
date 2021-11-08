import matplotlib.pyplot as plt
import networkx as nx

import nxviz as nv
from nxviz import annotate

G = nx.erdos_renyi_graph(n=30, p=0.1)
G = nx.relabel_nodes(G, {i: "long name #" + str(i) for i in range(len(G))})

nv.circos(G)
# the rotated labels take up more space, so we will have to increase the
# padding a bit. 15% on all sides works well here.
plt.tight_layout(rect=(0.15, 0.15, 0.85, 0.85))
annotate.circos_labels(G, layout="numbers")
plt.show()
