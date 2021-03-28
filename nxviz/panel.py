"""Declarative graph visualization panels."""
from nxviz import utils
import warnings
from itertools import combinations
import numpy as np


### Iterators to generate subgraphs.
def hive_triplets(G, group_by):
    """Yield subgraphs containing triplets of node categories.

    Intended for hive plotting.
    """
    nt = utils.node_table(G)
    groups = sorted(nt[group_by].unique())
    if len(groups) > 6:
        warnings.warn(
            "You have more than 6 groups of nodes, "
            "which means you might end up having a lot of subplots made. "
            "User beware! "
            "We recommend using hive plots only when you have 6 or fewer "
            "groups of nodes."
        )
    triplets = combinations(groups, 3)

    for groups in triplets:
        wanted_nodes = (n for n in G.nodes() if G.nodes[n][group_by] in groups)
        yield G.subgraph(wanted_nodes)


def edge_group(G, group_by):
    """Yield graphs containing only certain categories of edges."""
    et = utils.edge_table(G)
    groups = sorted(et[group_by].unique())
    for group in groups:
        G_sub = G.copy()
        G_sub.remove_edges_from(G_sub.edges())
        for u, v, d in G.edges(data=True):
            if d[group_by] == group:
                G_sub.add_edge(u, v, **d)
        yield G_sub


def node_group_edges(G, group_by):
    """Return a subgraph containing edges connected to a particular category of nodes."""
    nt = utils.node_table(G)
    groups = sorted(nt[group_by].unique())

    for group in groups:
        G_sub = G.copy()
        G_sub.remove_edges_from(G_sub.edges())

        wanted_nodes = (n for n in G.nodes() if G.nodes[n][group_by] == group)
        for node in wanted_nodes:
            for u, v, d in G.edges(node, data=True):
                G_sub.add_edge(u, v, **d)
        yield G_sub


def n_rows_cols(groups):
    nrows = ncols = int(np.ceil(np.sqrt(len(groups))))
    return nrows, ncols
