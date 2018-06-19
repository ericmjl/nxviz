from os import path as osp

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from nxviz.plots import CircosPlot

curr_path = osp.dirname(osp.abspath(__file__))


def load_crime_network():
    df = pd.read_csv(
        curr_path + "/moreno_crime/out.moreno_crime_crime",
        sep=" ",
        skiprows=2,
        header=None,
    )
    df = df[[0, 1]]
    df.columns = ["personID", "crimeID"]
    df.index += 1

    # Read in the role metadata
    roles = pd.read_csv(
        curr_path + "/moreno_crime/rel.moreno_crime_crime.person.role",
        header=None,
    )
    roles.columns = ["roles"]
    roles.index += 1

    # Add the edge data to the graph.
    G = nx.Graph()
    for r, d in df.join(roles).iterrows():
        pid = "p{0}".format(d["personID"])  # pid stands for "Person I.D."
        cid = "c{0}".format(d["crimeID"])  # cid stands for "Crime I.D."
        G.add_node(pid, bipartite="person")
        G.add_node(cid, bipartite="crime")
        G.add_edge(pid, cid, role=d["roles"])

    # Read in the gender metadata
    gender = pd.read_csv(
        curr_path + "/moreno_crime/ent.moreno_crime_crime.person.sex",
        header=None,
    )
    gender.index += 1
    for n, gender_code in gender.iterrows():
        nodeid = "p{0}".format(n)
        G.node[nodeid]["gender"] = gender_code[0]

    return G


G = load_crime_network()

# Annotate each node with connectivity score
for n in G.nodes():
    dcs = nx.degree_centrality(G)
    G.node[n]["connectivity"] = dcs[n]

# Make a CircosPlot of the bipartite graph
c = CircosPlot(
    G,
    node_grouping="bipartite",
    node_order="connectivity",
    node_color="bipartite",
)
c.draw()


# Make the "people" projection of the bipartite graph.
person_nodes = [n for n in G.nodes() if G.node[n]["bipartite"] == "person"]
pG = nx.bipartite.projection.projected_graph(G, person_nodes)

for n in pG.nodes():
    dcs = nx.degree_centrality(pG)
    pG.node[n]["connectivity"] = dcs[n]

c = CircosPlot(
    pG, node_grouping="gender", node_order="connectivity", node_color="gender"
)
c.draw()
plt.show()
