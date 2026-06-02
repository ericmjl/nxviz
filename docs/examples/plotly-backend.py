import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def build_graph():
    from itertools import cycle

    import networkx as nx
    import numpy as np

    import nxviz as nv

    categories = cycle(["sun", "moon", "stars"])
    ordinal = cycle([1, 2, 3, 4, 5])
    continuous = cycle(np.linspace(0, 3, 20))

    n, p = 71, 0.1
    G = nx.erdos_renyi_graph(n=n, p=p)
    for node in G.nodes():
        G.nodes[node]["group"] = next(categories)
        G.nodes[node]["value"] = next(ordinal)
    for u, v in G.edges():
        G.edges[u, v]["edge_value"] = next(continuous)
    G
    return G, nv


@app.cell(hide_code=True)
def matplotlib_circos(G, nv):
    ax = nv.circos(G, group_by="group", sort_by="value", node_color_by="group")
    ax
    return


@app.cell(hide_code=True)
def plotly_circos(G, nv):
    fig_circos = nv.circos(G, group_by="group", sort_by="value", node_color_by="group", backend="plotly")
    fig_circos
    return


@app.cell(hide_code=True)
def plotly_arc(G, nv):
    fig_arc = nv.arc(G, group_by="group", sort_by="value", node_color_by="group", backend="plotly")
    fig_arc
    return


@app.cell(hide_code=True)
def plotly_hive(G, nv):
    fig_hive = nv.hive(G, group_by="group", sort_by="value", node_color_by="group", backend="plotly")
    fig_hive
    return


@app.cell(hide_code=True)
def plotly_matrix(G, nv):
    fig_matrix = nv.matrix(G, group_by="group", sort_by="value", node_color_by="group", backend="plotly")
    fig_matrix
    return


if __name__ == "__main__":
    app.run()
