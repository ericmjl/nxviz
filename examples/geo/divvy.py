import networkx as nx
import matplotlib.pyplot as plt

from nxviz import GeoPlot

G = nx.read_gpickle("divvy.pkl")
print(list(G.nodes(data=True))[0])
G_new = G.copy()
for n1, n2, d in G.edges(data=True):
    if d["count"] < 200:
        G_new.remove_edge(n1, n2)

g = GeoPlot(
    G_new,
    node_lat="latitude",
    node_lon="longitude",
    node_color="dpcapacity",
    node_size=0.005,
)


g.draw()
plt.show()
