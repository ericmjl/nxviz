# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.8",
#     "matplotlib>=3.3.3",
#     "networkx>=2.5",
#     "nxviz",
# ]
# [tool.uv.sources]
# nxviz = { path = "../..", editable = true }
# ///
import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Annotating Node Labels on Arc Plots

    Author: Alireza Hosseini
    """)
    return


@app.cell
def _():
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
    return


if __name__ == "__main__":
    app.run()
