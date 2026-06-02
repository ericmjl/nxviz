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
    # Annotating Circos Plot Node Labels

    This example set was contributed by Alireza Hosseini.
    """)
    return


@app.cell
def _():
    from random import randint
    import matplotlib.pyplot as plt
    import networkx as nx
    import nxviz as nv
    from nxviz import annotate
    G = nx.erdos_renyi_graph(n=30, p=0.1)
    for _n, _d in G.nodes(data=True):
        G.nodes[_n]['group'] = randint(0, 5)
    G = nx.relabel_nodes(G, {i: 'long name #' + str(i) for i in range(len(G))})
    nv.circos(G, group_by='group', node_color_by='group')
    annotate.circos_labels(G, group_by='group', layout='rotate')
    plt.tight_layout(rect=(0.05, 0.05, 0.95, 0.95))
    # The rotated labels take up more space, so we will have to increase the
    # padding a bit. 5% on all sides works well here.
    plt.show()
    return annotate, nv, nx, plt, randint


@app.cell
def _(annotate, nv, nx, plt, randint):
    G_1 = nx.erdos_renyi_graph(n=30, p=0.1)
    for _n, _d in G_1.nodes(data=True):
        G_1.nodes[_n]['group'] = randint(0, 5)
    G_1 = nx.relabel_nodes(G_1, {i: 'long name #' + str(i) for i in range(len(G_1))})
    nv.circos(G_1, group_by='group', node_color_by='group')
    annotate.circos_labels(G_1, group_by='group', layout='numbers')
    plt.tight_layout(rect=(0.15, 0.15, 0.85, 0.85))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Custom color mapping circos nodes and edges

    This example shows how to customize the color mapping of nodes and edges in a Circos plot.

    The example is contributed by Kelvin Tuong.
    """)
    return


@app.cell
def _(nx):
    from itertools import cycle
    categories = ['sun', 'moon', 'stars', 'cloud', 'wheel', 'box', 'plant', 'chair', 'slippers', 'tablet', 'laptop', 'dishwasher', 'bicycle', 'piano', 'laptop']
    palette = ['#1f77b4', '#ff7f0e', '#279e68', '#d62728', '#aa40fc', '#8c564b', '#e377c2', '#b5bd61', '#17becf', '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', '#dbdb8d', '#9edae5', '#ad494a', '#8c6d31']
    categorical = cycle(categories[0:4])
    categories[0:4]
    many_categorical = cycle(categories)
    _n = 71
    p = 0.01
    G_2 = nx.erdos_renyi_graph(n=_n, p=p)
    legend_kwargs = {'ncol': 1, 'bbox_to_anchor': (1, 0.5), 'frameon': False, 'loc': 'center left'}
    for _n in G_2.nodes():
        G_2.nodes[_n]['group1'] = next(categorical)
        G_2.nodes[_n]['group2'] = next(many_categorical)
    for u, v in G_2.edges():
        G_2.edges[u, v]['edge_group1'] = next(categorical)
        G_2.edges[u, v]['edge_group2'] = next(many_categorical)
        G_2.edges[u, v]['thickness'] = 3
    return G_2, legend_kwargs, palette


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Current default behavior
    """)
    return


@app.cell
def _(G_2, annotate, legend_kwargs, nv):
    nv.circos(G_2, group_by='group1', node_color_by='group1')
    annotate.node_colormapping(G_2, color_by='group1', legend_kwargs=legend_kwargs)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can manusally specify the node colors:
    """)
    return


@app.cell
def _(G_2, nv, palette):
    nv.circos(G_2, group_by='group1', node_color_by='group1', node_palette=palette[:4])  # specify 4 colors for 4 groups
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    now with more than 12 categories (14), and a long color palette (20 colors)
    """)
    return


@app.cell
def _(G_2, nv, palette):
    nv.circos(G_2, group_by='group2', node_color_by='group2', node_palette=palette)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    same as above but limit to 7 colors - colors start to cycle if palette is provided as a list.
    """)
    return


@app.cell
def _(G_2, nv, palette):
    nv.circos(G_2, group_by='group2', node_color_by='group2', node_palette=palette[:7])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    palette provides as a dictionary
    """)
    return


@app.cell
def _(G_2, annotate, nv):
    pal = {'moon': 'red', 'stars': 'yellow', 'sun': 'black', 'cloud': 'blue'}
    nv.circos(G_2, group_by='group1', node_color_by='group1', node_palette=pal)
    annotate.node_colormapping(G_2, color_by='group1', palette=pal)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    order of keys don't matter
    """)
    return


@app.cell
def _(G_2, annotate, nv):
    pal_1 = {'moon': 'red', 'cloud': 'pink', 'stars': 'yellow', 'sun': 'black'}
    nv.circos(G_2, group_by='group1', node_color_by='group1', node_palette=pal_1)
    annotate.node_colormapping(G_2, color_by='group1', palette=pal_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    can mix colors/hex codes
    """)
    return


@app.cell
def _(G_2, annotate, nv):
    pal_2 = ['pink', '#1f77B4', 'green', '#ff7f0e']
    nv.circos(G_2, group_by='group1', node_color_by='group1', node_palette=pal_2)
    annotate.node_colormapping(G_2, color_by='group1', palette=pal_2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    swapping of order of colors in a list matters. But the plot should reflect this correctly - if you look up at the dictionary examples, the same order is preserved.
    """)
    return


@app.cell
def _(G_2, annotate, nv):
    pal_3 = ['pink', '#1f77B4', '#ff7f0e', 'green']  # swapped the order of the last two colours
    nv.circos(G_2, group_by='group1', node_color_by='group1', node_palette=pal_3)
    annotate.node_colormapping(G_2, color_by='group1', palette=pal_3)
    return (pal_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Can be used on edges as well:
    """)
    return


@app.cell
def _(G_2, annotate, nv, pal_3, palette):
    ax = nv.circos(G_2, group_by='group1', node_color_by='group1', edge_color_by='edge_group1', node_palette=pal_3, edge_palette=palette, edge_lw_by='thickness')
    annotate.edge_colormapping(G_2, color_by='edge_group1', palette=palette)  # not quite sure how to make both node and edge legend appear
    return


if __name__ == "__main__":
    app.run()
