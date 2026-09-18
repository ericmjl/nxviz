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
    # Matrix Plot

    Here is an example of how to create a matrix plot.
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %config InlineBackend.figure_format = 'retina'
    # magic command not supported in marimo; please file an issue to add support
    # %load_ext autoreload
    # '%autoreload 2' command supported automatically in marimo
    return


@app.cell
def _():
    import networkx as nx

    import nxviz as nv

    return nv, nx


@app.cell
def _(nv, nx):
    G = nx.lollipop_graph(m=10, n=4)
    for n, d in G.nodes(data=True):
        G.nodes[n]["degree"] = nx.degree(G, n)
    ax = nv.matrix(G, sort_by="degree", node_color_by="degree")
    return (G,)


@app.cell
def _(G, nx):
    nx.draw(G)
    return


if __name__ == "__main__":
    app.run()
