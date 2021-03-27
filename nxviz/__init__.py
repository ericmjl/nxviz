"""High level nxviz plotting API."""
from nxviz.plots import ArcPlot, CircosPlot, MatrixPlot, GeoPlot  # NOQA


from functools import partial, update_wrapper
from typing import Callable, Dict, Hashable

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from nxviz import edges, nodes
from nxviz.plots import aspect_equal, despine

# This docstring applies to all plotting functions in this module.
docstring = """High-level graph plotting function.

## Parameters

### Basic

- `G`: A NetworkX Graph.

### Nodes

- `group_by`: Node metadata attribute key to group nodes.
- `sort_by`: Node metadata attribute key to sort nodes.
- `node_color_by`: Node metadata attribute key to color nodes.
- `node_alpha_by`: Node metadata attribute key to set node transparency.
- `node_size_by`: Node metadata attribute key to set node size.
- `node_aes_kwargs`: Keyword arguments to set node aesthetics appearances.
    TODO: Elaborate on what these arguments are.

### Edges

- `edge_color_by`: Edge metdata attribute key to color edges.
- `edge_lw_by`: Edge metdata attribute key to set edge line width.
- `edge_alpha_by`: Edge metdata attribute key to set edge transparency.
- `edge_aes_kwargs`: Keyword arguments to set node aesthetics appearances.
    TODO: Elaborate on what these arguments are.
"""


def base(
    G: nx.Graph,
    node_layout_func: Callable,
    edge_line_func: Callable,
    group_by: Hashable,
    sort_by: Hashable,
    node_color_by: Hashable = None,
    node_alpha_by: Hashable = None,
    node_size_by: Hashable = None,
    node_aes_kwargs: Dict = {},
    edge_color_by: Hashable = None,
    edge_lw_by: Hashable = None,
    edge_alpha_by: Hashable = None,
    edge_aes_kwargs: Dict = {},
    node_layout_kwargs: Dict = {},
    edge_line_kwargs: Dict = {},
):

    pos = node_layout_func(
        G,
        group_by=group_by,
        sort_by=sort_by,
        color_by=node_color_by,
        size_by=node_size_by,
        alpha_by=node_alpha_by,
        aesthetics_kwargs=node_aes_kwargs,
        layout_kwargs=node_layout_kwargs,
    )
    edge_line_func(
        G,
        pos,
        color_by=edge_color_by,
        lw_by=edge_lw_by,
        alpha_by=edge_alpha_by,
        aesthetics_kwargs=edge_aes_kwargs,
    )

    despine()
    aspect_equal()
    return plt.gca()


base.__doc__ = docstring

arc = partial(
    base,
    node_layout_func=nodes.arc,
    edge_line_func=edges.arc,
    group_by=None,
    sort_by=None,
)
update_wrapper(arc, base)
circos = partial(
    base,
    node_layout_func=nodes.circos,
    edge_line_func=edges.circos,
    group_by=None,
    sort_by=None,
)
update_wrapper(circos, base)
parallel = partial(
    base,
    node_layout_func=nodes.parallel,
    edge_line_func=edges.line,
    sort_by=None,
    node_aes_kwargs={"size_scale": 0.5},
)
update_wrapper(parallel, base)


def base_cloned(
    G,
    node_layout_func,
    edge_line_func,
    group_by,
    sort_by=None,
    node_color_by=None,
    node_alpha_by=None,
    node_size_by=None,
    node_aes_kwargs={},
    edge_color_by=None,
    edge_lw_by=None,
    edge_alpha_by=None,
    edge_aes_kwargs={},
    node_layout_kwargs: Dict = {},
    edge_line_kwargs: Dict = {},
    cloned_node_layout_kwargs: Dict = {},
):
    """Base plotting function for visualizations that have cloned axes."""
    pos = node_layout_func(
        G,
        group_by=group_by,
        sort_by=sort_by,
        color_by=node_color_by,
        size_by=node_size_by,
        alpha_by=node_alpha_by,
        aesthetics_kwargs=node_aes_kwargs,
        layout_kwargs=node_layout_kwargs,
    )
    pos_cloned = node_layout_func(
        G,
        group_by=group_by,
        sort_by=sort_by,
        color_by=node_color_by,
        size_by=node_size_by,
        alpha_by=node_alpha_by,
        aesthetics_kwargs=node_aes_kwargs,
        layout_kwargs=cloned_node_layout_kwargs,
    )
    edge_line_func(
        G,
        pos,
        pos_cloned=pos_cloned,
        color_by=edge_color_by,
        lw_by=edge_lw_by,
        alpha_by=edge_alpha_by,
        aesthetics_kwargs=edge_aes_kwargs,
        **edge_line_kwargs,
    )

    despine()
    aspect_equal()
    return plt.gca()


base_cloned.__doc__ = docstring


hive = partial(
    base_cloned,
    node_layout_func=nodes.hive,
    edge_line_func=edges.hive,
    cloned_node_layout_kwargs={"rotation": np.pi / 6},
)
update_wrapper(hive, base_cloned)
matrix = partial(
    base_cloned,
    group_by=None,
    node_layout_func=nodes.matrix,
    edge_line_func=edges.matrix,
    cloned_node_layout_kwargs={"axis": "y"},
    edge_line_kwargs={"directed": False},
)
update_wrapper(matrix, base_cloned)
