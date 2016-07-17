from nxviz.circos import CircosPlot
import networkx as nx

G = nx.octahedral_graph()
c = CircosPlot(G.nodes(), G.edges(), radius=5, node_radius=1)
c.draw()
