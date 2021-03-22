import janitor
import networkx as nx
from .utils import edge_table, node_table
from . import layouts
import pandas as pd
from datashader.bundling import hammer_bundle
from .colors import node_colors
import matplotlib.pyplot as plt
from typing import Dict
from matplotlib.patches import Path

from matplotlib import patches


def bundle(G, pos, ax=None, edge_kwargs={}):
    edge_df = edge_table(G)
    node_df = (
        pd.DataFrame(pos)
        .T.reset_index()
        .rename_columns({0: "x", 1: "y", "index": "name"})
    )
    hb = hammer_bundle(nodes=node_df, edges=edge_df)
    if ax is None:
        ax = plt.gca()
    kwargs = dict(color="black", alpha=0.1)
    kwargs.update(edge_kwargs)
    ax = hb.plot(x="x", y="y", ax=ax, zorder=0, **kwargs)
    ax.legend().remove()





def circos_curves(G: nx.Graph, pos: Dict, ax=None, edge_kwargs={}):
    if ax is None:
        ax = plt.gca()
    for start, end in G.edges():
        verts = [pos[start], (0, 0), pos[end]]
        color = "black"
        codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        lw = 1
        path = Path(verts, codes)
        patch = patches.PathPatch(
            path, lw=lw, edgecolor=color, zorder=1, facecolor="none", alpha=0.1
        )
        ax.add_patch(patch)


def lines(G: nx.Graph, pos: Dict, ax=None, edge_kwargs={}):
    if ax is None:
        ax = plt.gca()
    ek = dict()
    ek.update(edge_kwargs)
    ek["alpha"] = 0.1

    nx.draw_networkx_edges(G, pos, ax=ax, **ek)
