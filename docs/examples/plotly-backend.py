import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def intro_md():
    import marimo as mo

    mo.md(
        "# Plotly Backend for nxviz\n\nThis notebook demonstrates the **Plotly backend** for nxviz, providing interactive network visualizations.\n\nWe will build a random graph with categorical and continuous node/edge attributes, then render it using both matplotlib and Plotly backends for comparison."
    )
    return (mo,)


@app.cell(hide_code=True)
def md_build(mo):
    mo.md("""
    ## Build the Graph

    We construct an Erdos-Renyi random graph with 71 nodes and edge probability 0.1. Each node gets a categorical `group` attribute (sun/moon/stars) and an ordinal `value`. Edges receive a continuous `edge_value`.
    """)
    return


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
def md_mpl(mo):
    mo.md("""
    ## Matplotlib Circos (Reference)

    The familiar matplotlib-based circos plot, shown here for comparison with the Plotly versions below.
    """)
    return


@app.cell(hide_code=True)
def matplotlib_circos(G, nv):
    ax = nv.circos(G, group_by="group", sort_by="value", node_color_by="group")
    ax
    return


@app.cell(hide_code=True)
def md_plotly_circos(mo):
    mo.md("""
    ## Plotly Circos

    The same circos plot rendered with the **Plotly backend**. Try hovering over nodes and edges, and use the Plotly toolbar to zoom and pan.
    """)
    return


@app.cell(hide_code=True)
def plotly_circos(G, nv):
    fig_circos = nv.circos(
        G,
        group_by="group",
        sort_by="value",
        node_color_by="group",
        backend="plotly",
    )
    fig_circos
    return


@app.cell(hide_code=True)
def md_plotly_arc(mo):
    mo.md("""
    ## Plotly Arc

    An arc diagram rendered with Plotly. Arc plots are useful for visualizing connectivity patterns along a single axis.
    """)
    return


@app.cell(hide_code=True)
def plotly_arc(G, nv):
    fig_arc = nv.arc(
        G,
        group_by="group",
        sort_by="value",
        node_color_by="group",
        backend="plotly",
    )
    fig_arc
    return


@app.cell(hide_code=True)
def md_plotly_hive(mo):
    mo.md("""
    ## Plotly Hive

    A hive plot rendered with Plotly. Hive plots arrange nodes along radial axes grouped by category, making structural patterns more apparent.
    """)
    return


@app.cell(hide_code=True)
def plotly_hive(G, nv):
    fig_hive = nv.hive(
        G,
        group_by="group",
        sort_by="value",
        node_color_by="group",
        backend="plotly",
    )
    fig_hive
    return


@app.cell(hide_code=True)
def md_plotly_matrix(mo):
    mo.md("""
    ## Plotly Matrix

    A matrix plot rendered with Plotly. Matrix plots reveal adjacency structure at a glance, with nodes sorted by group and value.
    """)
    return


@app.cell(hide_code=True)
def plotly_matrix(G, nv):
    fig_matrix = nv.matrix(
        G,
        group_by="group",
        sort_by="value",
        node_color_by="group",
        backend="plotly",
    )
    fig_matrix
    return


if __name__ == "__main__":
    app.run()
