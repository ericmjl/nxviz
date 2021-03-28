"""High level nxviz plotting API."""


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
geo = partial(
    base,
    node_layout_func=nodes.geo,
    edge_line_func=edges.line,
    group_by=None,
    sort_by=None,
    node_aes_kwargs={"size_scale": 0.0015},
)


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


# Object-oriented API below, placed for compatibility.


class BasePlot:
    def __init__(
        self,
        G: nx.Graph = None,
        node_grouping: Hashable = None,
        node_order: Hashable = None,
        node_color: Hashable = None,
        node_alpha: Hashable = None,
        node_size: Hashable = None,
        nodeprops: Dict = None,
        edge_color: Hashable = None,
        edge_alpha: Hashable = None,
        edge_width: Hashable = None,
        edgeprops: Dict = None,
    ):
        """Instantiate a plot.

        ## Parameters:

        - `G`: NetworkX graph to plot.
        - `node_grouping`: The node attribute on which to specify the grouping position of nodes.
        - `node_order`: The node attribute on which to specify the coloring of nodes.
        - `node_color`: The node attribute on which to specify the colour of nodes.
        - `node_alpha`: The node attribute on which to specify the transparency of nodes.
        - `node_size`: The node attribute on which to specify the size of nodes.
        - `nodeprops`: A `matplotlib`-compatible `props` dictionary.
        - `edge_color`: The edge attribute on which to specify the colour of edges.
        - `edge_alpha`: The edge attribute on which to specify the transparency of edges.
        - `edge_width`: The edge attribute on which to specify the width of edges.
        - `edgeprops`: A `matplotlib-compatible `props` dictionary.
        """
        import warnings

        warnings.warn(
            "As of nxviz 0.7, the object-oriented API is being deprecated "
            "in favour of a functional API. "
            "Please consider switching your plotting code! "
            "The object-oriented API wrappers remains in place "
            "to help you transition over. "
            "A few changes between the old and new API exist; "
            "please consult the nxviz documentation for more information. "
            "When the 1.0 release of nxviz happens, "
            "the object-oriented API will be dropped entirely."
        )

    def draw():
        """No longer implemented!"""
        pass


functional_api_names = [
    "group_by",
    "sort_by",
    "node_color_by",
    "node_alpha_by",
    "node_size_by",
    "node_aes_kwargs",
    "edge_color_by",
    "edge_alpha_by",
    "edge_lw_by",
    "edge_aes_kwargs",
]

object_api_names = [
    "node_grouping",
    "node_order",
    "node_color",
    "node_alpha",
    "node_size",
    "nodeprops",
    "edge_color",
    "edge_alpha",
    "edge_width",
    "edgeprops",
]

functional_to_object = dict(zip(functional_api_names, object_api_names))
object_to_functional = dict(zip(object_api_names, functional_api_names))


class ArcPlot(BasePlot):
    def __init__(self, G, **kwargs):
        super().__init__()
        func_kwargs = {object_to_functional[k]: v for k, v in kwargs.items()}
        self.fig = plt.figure()
        self.ax = arc(G, **func_kwargs)


class CircosPlot(BasePlot):
    def __init__(self, G, **kwargs):
        super().__init__()
        func_kwargs = {object_to_functional[k]: v for k, v in kwargs.items()}
        self.fig = plt.figure()
        self.ax = circos(G, **func_kwargs)


class HivePlot(BasePlot):
    def __init__(self, G, **kwargs):
        super().__init__()
        func_kwargs = {object_to_functional[k]: v for k, v in kwargs.items()}
        self.fig = plt.figure()
        self.ax = hive(G, **func_kwargs)


class MatrixPlot(BasePlot):
    def __init__(self, G, **kwargs):
        super().__init__()
        func_kwargs = {object_to_functional[k]: v for k, v in kwargs.items()}
        self.fig = plt.figure()
        self.ax = matrix(G, **func_kwargs)
