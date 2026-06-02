"""High level nxviz plotting API."""

from copy import deepcopy
from functools import partial, update_wrapper
from typing import Callable, Dict, Hashable, List, Optional, Union

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from nxviz import edges, nodes
from nxviz.plots import aspect_equal, despine


def backend_plot(
    G: nx.Graph,
    node_layout_func: Callable,
    edge_line_func: Callable,
    group_by: Hashable,
    sort_by: Hashable,
    node_color_by: Hashable = None,
    node_alpha_by: Hashable = None,
    node_size_by: Hashable = None,
    node_enc_kwargs: Dict = {},
    edge_color_by: Hashable = None,
    edge_lw_by: Hashable = None,
    edge_alpha_by: Hashable = None,
    edge_enc_kwargs: Dict = {},
    node_layout_kwargs: Dict = {},
    edge_line_kwargs: Dict = {},
    node_palette: Optional[Union[Dict, List]] = None,
    edge_palette: Optional[Union[Dict, List]] = None,
    backend_obj=None,
    pos_cloned=None,
    cloned_node_layout_kwargs: Dict = {},
    line_type: str = "circos",
):
    """Render a plot using a backend object (non-matplotlib path)."""
    from nxviz import encodings, paths
    from nxviz.utils import edge_table, node_table

    nt = node_table(G)

    layout_func = node_layout_func
    from functools import partial as _p

    if isinstance(layout_func, partial):
        layout_func_inner = layout_func.func
        fixed_kwargs = layout_func.keywords
        layout_func_to_use = _p(layout_func_inner, **fixed_kwargs)
    else:
        layout_func_to_use = layout_func

    from nxviz import layouts

    if isinstance(layout_func_to_use, partial):
        actual_layout = layout_func_to_use.args[0] if layout_func_to_use.args else None
    else:
        actual_layout = None

    pos = node_layout_func.keywords.get("layout_func", layouts.circos)
    if isinstance(pos, partial):
        pass

    layout_func_resolved = resolve_layout_func(node_layout_func)
    rescale_func_resolved = resolve_rescale_func(node_layout_func)

    pos = layout_func_resolved(nt, group_by, sort_by, **node_layout_kwargs)

    node_color = nodes.node_colors(nt, node_color_by, node_palette)
    enc_kw = deepcopy(node_enc_kwargs)
    alpha_bounds = enc_kw.pop("alpha_bounds", None)
    alpha = nodes.transparency(nt, node_alpha_by, alpha_bounds) * enc_kw.pop(
        "alpha_scale", 1
    )
    size = nodes.node_size(nt, node_size_by) * enc_kw.pop("size_scale", 1)

    axes = backend_obj.create_axes()

    backend_obj.draw_nodes(
        axes, nt, pos, node_color, alpha, size, encodings_kwargs=enc_kw
    )

    et = edge_table(G)
    ntc = node_table(G)
    edges.validate_color_by(G, edge_color_by, node_color_by)
    edge_color = edges.edge_colors(et, ntc, edge_color_by, node_color_by, edge_palette)
    enc_kw_edge = deepcopy(edge_enc_kwargs)
    lw = edges.line_width(et, edge_lw_by) * enc_kw_edge.pop("lw_scale", 1.0)
    alpha_bounds_e = enc_kw_edge.pop("alpha_bounds", None)
    edge_alpha = edges.transparency(et, edge_alpha_by, alpha_bounds_e) * enc_kw_edge.pop(
        "alpha_scale", 1.0
    )

    if pos_cloned is not None:
        pass
    elif cloned_node_layout_kwargs:
        pos_cloned = layout_func_resolved(
            nt, group_by, sort_by, **cloned_node_layout_kwargs
        )

    if line_type == "circos":
        path_coords = paths.circos_coords(et, pos)
    elif line_type == "line":
        path_coords = paths.line_coords(et, pos)
    elif line_type == "arc":
        path_coords = paths.arc_coords(et, pos)
    elif line_type == "hive":
        path_coords = paths.hive_coords(et, pos, pos_cloned)
    elif line_type == "matrix":
        path_coords = paths.matrix_coords(et, pos, pos_cloned)
    else:
        path_coords = paths.line_coords(et, pos)

    aes_kw = {"facecolor": "none"}
    aes_kw.update(enc_kw_edge)

    backend_obj.draw_edges(
        axes,
        et,
        pos,
        path_coords,
        edge_color,
        edge_alpha,
        lw,
        line_type,
        pos_cloned=pos_cloned,
        aes_kw=aes_kw,
    )

    plot_type_for_rescale = "default"
    if line_type == "arc":
        plot_type_for_rescale = "arc"
    elif line_type in ("hive",):
        plot_type_for_rescale = "square"

    backend_obj.despine(axes)
    backend_obj.set_aspect_equal(axes)
    backend_obj.rescale(axes, pos, plot_type_for_rescale)

    return backend_obj.get_figure(axes)


def resolve_layout_func(node_layout_func):
    """Extract the actual layout function from a partial of nodes.draw."""
    from nxviz import layouts

    if isinstance(node_layout_func, partial):
        fixed_kw = node_layout_func.keywords
        return fixed_kw.get("layout_func", layouts.circos)
    return layouts.circos


def resolve_rescale_func(node_layout_func):
    """Extract the rescale function from a partial of nodes.draw."""
    from nxviz.plots import rescale

    if isinstance(node_layout_func, partial):
        fixed_kw = node_layout_func.keywords
        return fixed_kw.get("rescale_func", rescale)
    return rescale


def base(
    G: nx.Graph,
    node_layout_func: Callable,
    edge_line_func: Callable,
    group_by: Hashable,
    sort_by: Hashable,
    node_color_by: Hashable = None,
    node_alpha_by: Hashable = None,
    node_size_by: Hashable = None,
    node_enc_kwargs: Dict = {},
    edge_color_by: Hashable = None,
    edge_lw_by: Hashable = None,
    edge_alpha_by: Hashable = None,
    edge_enc_kwargs: Dict = {},
    node_layout_kwargs: Dict = {},
    edge_line_kwargs: Dict = {},
    node_palette: Optional[Union[Dict, List]] = None,
    edge_palette: Optional[Union[Dict, List]] = None,
    backend: str = "matplotlib",
):
    """High-level graph plotting function.

    ## Parameters

    ### Basic

    - `G`: A NetworkX Graph.

    ### Nodes

    - `group_by`: Node metadata attribute key to group nodes.
    - `sort_by`: Node metadata attribute key to sort nodes.
    - `node_color_by`: Node metadata attribute key to color nodes.
    - `node_alpha_by`: Node metadata attribute key to set node transparency.
    - `node_size_by`: Node metadata attribute key to set node size.
    - `node_enc_kwargs`: Keyword arguments to set node visual encodings.
        TODO: Elaborate on what these arguments are.
    - `node_palette`: Optional custom palette of colours for plotting categorical groupings
        in a list/dictionary. Colours must be values `matplotlib.colors.ListedColormap`
        can interpret. If a dictionary is provided, key and record corresponds to
        category and colour respectively.

    ### Edges

    - `edge_color_by`: Edge metdata attribute key to color edges.
        There are two special value for this parameter
        when using directed graphs:
        "source_node_color" and "target_node_color".
        If these values are set, then `node_color_by` also needs to be set.
    - `edge_lw_by`: Edge metdata attribute key to set edge line width.
    - `edge_alpha_by`: Edge metdata attribute key to set edge transparency.
    - `edge_enc_kwargs`: Keyword arguments to set edge visual encodings.
    - `edge_palette`: Same as node_palette but for edges.
        TODO: Elaborate on what these arguments are.

    ### Backend

    - `backend`: Rendering backend to use. Options: "matplotlib" (default), "plotly".
    """
    line_type = get_line_type(edge_line_func)

    if backend != "matplotlib":
        from nxviz.backend import get_backend

        backend_obj = get_backend(backend)
        return backend_plot(
            G,
            node_layout_func=node_layout_func,
            edge_line_func=edge_line_func,
            group_by=group_by,
            sort_by=sort_by,
            node_color_by=node_color_by,
            node_alpha_by=node_alpha_by,
            node_size_by=node_size_by,
            node_enc_kwargs=node_enc_kwargs,
            edge_color_by=edge_color_by,
            edge_lw_by=edge_lw_by,
            edge_alpha_by=edge_alpha_by,
            edge_enc_kwargs=edge_enc_kwargs,
            node_layout_kwargs=node_layout_kwargs,
            edge_line_kwargs=edge_line_kwargs,
            node_palette=node_palette,
            edge_palette=edge_palette,
            backend_obj=backend_obj,
            line_type=line_type,
        )

    pos = node_layout_func(
        G,
        group_by=group_by,
        sort_by=sort_by,
        color_by=node_color_by,
        size_by=node_size_by,
        alpha_by=node_alpha_by,
        encodings_kwargs=node_enc_kwargs,
        layout_kwargs=node_layout_kwargs,
        palette=node_palette,
    )
    edge_line_func(
        G,
        pos,
        color_by=edge_color_by,
        node_color_by=node_color_by,
        lw_by=edge_lw_by,
        alpha_by=edge_alpha_by,
        encodings_kwargs=edge_enc_kwargs,
        palette=edge_palette,
    )

    despine()
    aspect_equal()
    return plt.gca()


def get_line_type(edge_line_func: Callable) -> str:
    """Determine the line type from the edge line function."""
    if isinstance(edge_line_func, partial):
        func_name = getattr(edge_line_func, "__name__", "")
        if "circos" in func_name:
            return "circos"
        elif "arc" in func_name:
            return "arc"
        elif "hive" in func_name:
            return "hive"
        elif "matrix" in func_name:
            return "matrix"
        elif "line" in func_name:
            return "line"

        lines_func = edge_line_func.keywords.get("lines_func")
        if lines_func is not None:
            lf_name = getattr(lines_func, "__name__", "")
            if "circos" in lf_name:
                return "circos"
            elif "arc" in lf_name:
                return "arc"
            elif "hive" in lf_name:
                return "hive"
            elif "matrix" in lf_name:
                return "matrix"
    return "line"


arc = partial(
    base,
    node_layout_func=nodes.arc,
    edge_line_func=edges.arc,
    group_by=None,
    sort_by=None,
)
update_wrapper(arc, base)
arc.__name__ = "api.arc"

circos = partial(
    base,
    node_layout_func=nodes.circos,
    edge_line_func=edges.circos,
    group_by=None,
    sort_by=None,
)
update_wrapper(circos, base)
circos.__name__ = "api.circos"

parallel = partial(
    base,
    node_layout_func=nodes.parallel,
    edge_line_func=edges.line,
    sort_by=None,
    node_enc_kwargs={"size_scale": 0.5},
)
update_wrapper(parallel, base)
parallel.__name__ = "api.parallel"

geo = partial(
    base,
    node_layout_func=nodes.geo,
    edge_line_func=edges.line,
    group_by=None,
    sort_by=None,
    node_enc_kwargs={"size_scale": 0.0015},
)
update_wrapper(geo, base)
geo.__name__ = "api.geo"


def base_cloned(
    G,
    node_layout_func,
    edge_line_func,
    group_by,
    sort_by=None,
    node_color_by=None,
    node_alpha_by=None,
    node_size_by=None,
    node_enc_kwargs={},
    edge_color_by=None,
    edge_lw_by=None,
    edge_alpha_by=None,
    edge_enc_kwargs={},
    node_layout_kwargs: Dict = {},
    edge_line_kwargs: Dict = {},
    cloned_node_layout_kwargs: Dict = {},
    node_palette: Optional[Union[Dict, List]] = None,
    edge_palette: Optional[Union[Dict, List]] = None,
    backend: str = "matplotlib",
):
    """High-level graph plotting function.

    ## Parameters

    ### Basic

    - `G`: A NetworkX Graph.

    ### Nodes

    - `group_by`: Node metadata attribute key to group nodes.
    - `sort_by`: Node metadata attribute key to sort nodes.
    - `node_color_by`: Node metadata attribute key to color nodes.
    - `node_alpha_by`: Node metadata attribute key to set node transparency.
    - `node_size_by`: Node metadata attribute key to set node size.
    - `node_enc_kwargs`: Keyword arguments to set node visual encodings.
        TODO: Elaborate on what these arguments are.
    - `node_palette`: Optional custom palette of colours for plotting categorical groupings
        in a list/dictionary. Colours must be values `matplotlib.colors.ListedColormap`
        can interpret. If a dictionary is provided, key and record corresponds to
        category and colour respectively.

    ### Edges

    - `edge_color_by`: Edge metdata attribute key to color edges.
        There are two special value for this parameter
        when using directed graphs:
        "source_node_color" and "target_node_color".
        If these values are set, then `node_color_by` also needs to be set.
    - `edge_lw_by`: Edge metdata attribute key to set edge line width.
    - `edge_alpha_by`: Edge metdata attribute key to set edge transparency.
    - `edge_enc_kwargs`: Keyword arguments to set edge visual encodings.
    - `edge_palette`: Same as node_palette but for edges.

    ### Backend

    - `backend`: Rendering backend to use. Options: "matplotlib" (default), "plotly".
    """
    line_type = get_line_type(edge_line_func)

    if backend != "matplotlib":
        from nxviz.backend import get_backend

        backend_obj = get_backend(backend)
        return backend_plot(
            G,
            node_layout_func=node_layout_func,
            edge_line_func=edge_line_func,
            group_by=group_by,
            sort_by=sort_by,
            node_color_by=node_color_by,
            node_alpha_by=node_alpha_by,
            node_size_by=node_size_by,
            node_enc_kwargs=node_enc_kwargs,
            edge_color_by=edge_color_by,
            edge_lw_by=edge_lw_by,
            edge_alpha_by=edge_alpha_by,
            edge_enc_kwargs=edge_enc_kwargs,
            node_layout_kwargs=node_layout_kwargs,
            edge_line_kwargs=edge_line_kwargs,
            node_palette=node_palette,
            edge_palette=edge_palette,
            backend_obj=backend_obj,
            cloned_node_layout_kwargs=cloned_node_layout_kwargs,
            line_type=line_type,
        )

    pos = node_layout_func(
        G,
        group_by=group_by,
        sort_by=sort_by,
        color_by=node_color_by,
        size_by=node_size_by,
        alpha_by=node_alpha_by,
        encodings_kwargs=node_enc_kwargs,
        layout_kwargs=node_layout_kwargs,
        palette=node_palette,
    )
    pos_cloned = node_layout_func(
        G,
        group_by=group_by,
        sort_by=sort_by,
        color_by=node_color_by,
        size_by=node_size_by,
        alpha_by=node_alpha_by,
        encodings_kwargs=node_enc_kwargs,
        layout_kwargs=cloned_node_layout_kwargs,
        palette=node_palette,
    )
    edge_line_func(
        G,
        pos,
        pos_cloned=pos_cloned,
        color_by=edge_color_by,
        node_color_by=node_color_by,
        lw_by=edge_lw_by,
        alpha_by=edge_alpha_by,
        encodings_kwargs=edge_enc_kwargs,
        palette=edge_palette,
        **edge_line_kwargs,
    )

    despine()
    aspect_equal()
    return plt.gca()


hive = partial(
    base_cloned,
    node_layout_func=nodes.hive,
    edge_line_func=edges.hive,
    cloned_node_layout_kwargs={"rotation": np.pi / 6},
)
update_wrapper(hive, base_cloned)
hive.__name__ = "api.hive"

matrix = partial(
    base_cloned,
    group_by=None,
    node_layout_func=nodes.matrix,
    edge_line_func=edges.matrix,
    cloned_node_layout_kwargs={"axis": "y"},
)
update_wrapper(matrix, base_cloned)
matrix.__name__ = "api.matrix"


# Object-oriented API below, placed for compatibility.


class BasePlot:
    """Base Plot class."""

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
        node_palette: Optional[Union[Dict, List]] = None,
        edge_palette: Optional[Union[Dict, List]] = None,
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
        - `node_palette`: Optional custom palette of colours for plotting categorical groupings
        in a list/dictionary. Colours must be values `matplotlib.colors.ListedColormap`
        can interpret. If a dictionary is provided, key and record corresponds to
        category and colour respectively.
        - `edge_palette`: Same as node_palette but for edges.
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
    "node_enc_kwargs",
    "edge_color_by",
    "edge_alpha_by",
    "edge_lw_by",
    "edge_enc_kwargs",
    "node_palette",
    "edge_palette",
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
    "node_palette",
    "edge_palette",
]

functional_to_object = dict(zip(functional_api_names, object_api_names))
object_to_functional = dict(zip(object_api_names, functional_api_names))


class ArcPlot(BasePlot):
    """Arc Plot."""

    def __init__(self, G, **kwargs):
        super().__init__()
        func_kwargs = {object_to_functional[k]: v for k, v in kwargs.items()}
        self.fig = plt.figure()
        self.ax = arc(G, **func_kwargs)


class CircosPlot(BasePlot):
    """Circos Plot."""

    def __init__(self, G, **kwargs):
        super().__init__()
        func_kwargs = {object_to_functional[k]: v for k, v in kwargs.items()}
        self.fig = plt.figure()
        self.ax = circos(G, **func_kwargs)


class HivePlot(BasePlot):
    """Hive Plot."""

    def __init__(self, G, **kwargs):
        super().__init__()
        func_kwargs = {object_to_functional[k]: v for k, v in kwargs.items()}
        self.fig = plt.figure()
        self.ax = hive(G, **func_kwargs)


class MatrixPlot(BasePlot):
    """Matrix Plot."""

    def __init__(self, G, **kwargs):
        super().__init__()
        func_kwargs = {object_to_functional[k]: v for k, v in kwargs.items()}
        self.fig = plt.figure()
        self.ax = matrix(G, **func_kwargs)
