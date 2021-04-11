"""Declarative graph visualization facets.

There are two groups of functions in here:
One are intended to yield graph objects that
contain the subset of nodes and edges to be plotted.
The others are faceting functions that can be called on.
The faceting functions rely on the high level API for plotting.
"""
import warnings
from functools import partial, update_wrapper
from itertools import combinations
from typing import Callable, Hashable

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from nxviz import annotate, api, utils


### Iterators to generate subgraphs.
def hive_triplets(G: nx.Graph, group_by: Hashable):
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
        yield G.subgraph(wanted_nodes), groups


def edge_group(G: nx.Graph, group_by: Hashable):
    """Yield graphs containing only certain categories of edges."""
    et = utils.edge_table(G)
    groups = sorted(et[group_by].unique())
    for group in groups:
        G_sub = G.copy()
        G_sub.remove_edges_from(G_sub.edges())
        for u, v, d in G.edges(data=True):
            if d[group_by] == group:
                G_sub.add_edge(u, v, **d)
        yield G_sub, group


def node_group_edges(G: nx.Graph, group_by: Hashable):
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
        yield G_sub, group


def n_rows_cols(groups):
    """Return squarest n_rows and n_cols combination."""
    nrows = ncols = int(np.ceil(np.sqrt(len(groups))))
    return nrows, ncols


def null(*args, **kwargs):
    """A passthrough function that does nothing."""
    pass


grouping_annotations = {
    "api.circos": annotate.circos_group,
    "api.arc": annotate.arc_group,
    "api.matrix": annotate.matrix_block,
    "api.hive": annotate.hive_group,
    "api.parallel": annotate.parallel_group,
}

node_color_annotations = {
    "api.hive": null,
    "api.circos": annotate.node_colormapping,
    "api.matrix": annotate.node_colormapping,
    "api.arc": annotate.node_colormapping,
    "api.parallel": annotate.node_colormapping,
}


def facet_plot(
    G: nx.Graph,
    plotting_func: Callable,
    node_facet_func: Callable,
    node_group_by: Hashable,
    node_sort_by: Hashable,
    node_color_by: Hashable,
    edge_facet_func: Callable,
    edge_group_by: Hashable,
    edge_color_by: Hashable,
):
    """Generic facet plotting function.

    All faceting funcs should take G and group_by and yield graphs.
    Underneath the hood, how they work shouldn't be of concern.

    Edge facet func takes priority if both node and edge facet func are specified.
    Just keep this in mind.

    ## Parameters

    - `G`: The graph to facet.
    - `plotting_func`: One of the high level API functions to use for plotting.
    - `node_facet_func`: A function to facet the nodes by.
    - `node_group_by`: Node metadata attribute to group nodes by.
    - `node_sort_by`: Node metadata attribute to sort nodes by.
    - `node_color_by`: Node metadata attribute to color nodes by.
    - `edge_facet_func`: A function to facet the edges by.
    - `edge_group_by`: Edge metadata attribute to group edges by.
    - `edge_color_by`: Edge metadata attribute to color edges by.
    """
    group_by = node_group_by
    facet_func = node_facet_func
    if edge_facet_func and edge_group_by:
        group_by = edge_group_by
        facet_func = edge_facet_func

    graphs, groups = zip(*facet_func(G, group_by))
    nrows, ncols = n_rows_cols(groups)
    fig, axes = plt.subplots(figsize=(3 * nrows, 3 * ncols), nrows=nrows, ncols=ncols)
    axes = list(axes.flatten())

    for G_sub, group, ax in zip(graphs, groups, axes):
        plt.sca(ax)
        plotting_func(
            G_sub,
            group_by=node_group_by,
            sort_by=node_sort_by,
            node_color_by=node_color_by,
            edge_color_by=edge_color_by,
        )
        if node_group_by:
            grouping_annotations.get(plotting_func.__name__)(
                G_sub, group_by=node_group_by
            )
        if node_color_by:
            # Annotate only on the left most axes
            idx = axes.index(ax)
            if not idx % nrows:
                node_color_annotations[plotting_func.__name__](G, node_color_by)
        ax.set_title(f"{group_by} = {group}")

    last_idx = axes.index(ax)
    for ax in axes[last_idx + 1 :]:
        fig.delaxes(ax)
    plt.tight_layout()


#### Function begins below. This belongs to the "edge faceting" category.

hive_panel = partial(
    facet_plot,
    plotting_func=api.hive,
    node_facet_func=hive_triplets,
    node_sort_by=None,
    node_color_by=None,
    edge_facet_func=None,
    edge_group_by=None,
    edge_color_by=None,
)
update_wrapper(hive_panel, facet_plot)
hive_panel.__name__ = "facet.hive_panel"

matrix_panel = partial(
    facet_plot,
    plotting_func=api.matrix,
    node_facet_func=None,
    node_group_by=None,
    node_sort_by=None,
    node_color_by=None,
    edge_facet_func=edge_group,
    edge_color_by=None,
)
update_wrapper(matrix_panel, facet_plot)
matrix_panel.__name__ = "facet.matrix_panel"

arc_panel = partial(
    facet_plot,
    plotting_func=api.arc,
    node_facet_func=None,
    node_group_by=None,
    node_sort_by=None,
    node_color_by=None,
    edge_facet_func=edge_group,
    edge_color_by=None,
)
update_wrapper(arc_panel, facet_plot)
arc_panel.__name__ = "facet.arc_panel"

circos_panel = partial(
    facet_plot,
    plotting_func=api.circos,
    node_facet_func=None,
    node_group_by=None,
    node_sort_by=None,
    node_color_by=None,
    edge_facet_func=edge_group,
    edge_color_by=None,
)
update_wrapper(circos_panel, facet_plot)
circos_panel.__name__ = "facet.circos_panel"

parallel_panel = partial(
    facet_plot,
    plotting_func=api.parallel,
    node_facet_func=None,
    node_group_by=None,
    node_sort_by=None,
    node_color_by=None,
    edge_facet_func=edge_group,
    edge_color_by=None,
)
update_wrapper(parallel_panel, facet_plot)
parallel_panel.__name__ = "facet.parallel_panel"
