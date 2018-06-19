from os import path as osp

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from nxviz.plots import ArcPlot, CircosPlot

curr_path = osp.dirname(osp.abspath(__file__))


def load_physicians_network():
    # Read the edge list

    df = pd.read_csv(
        curr_path + "/moreno_innovation/out.moreno_innovation_innovation",
        sep=" ",
        skiprows=2,
        header=None,
    )
    df = df[[0, 1]]
    df.columns = ["doctor1", "doctor2"]

    G = nx.Graph()
    G.add_edges_from(zip(df["doctor1"], df["doctor2"]))

    return G


G = load_physicians_network()

# Make a CircosPlot, but with the nodes colored by their connected component
# subgraph ID.
ccs = nx.connected_component_subgraphs(G)
for i, g in enumerate(ccs):
    for n in g.nodes():
        G.node[n]["group"] = i
        G.node[n]["connectivity"] = G.degree(n)
m = CircosPlot(
    G, node_color="group", node_grouping="group", node_order="connectivity"
)
m.draw()
plt.show()


# Make an ArcPlot.
a = ArcPlot(
    G, node_color="group", node_grouping="group", node_order="connectivity"
)
a.draw()
plt.show()
