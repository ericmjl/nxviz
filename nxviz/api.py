"""High level nxviz plotting API."""

from copy import deepcopy
from functools import partial, update_wrapper
from typing import Callable, Dict, Hashable, List, Optional, Union

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from nxviz import edges, nodes
from nxviz.plots import aspect_equal, despine
from nxviz.polcart import to_cartesian


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
    from nxviz import paths
    from nxviz.utils import edge_table, node_table

    nt = node_table(G)

    layout_func_resolved = resolve_layout_func(node_layout_func)

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
    edge_alpha = edges.transparency(
        et, edge_alpha_by, alpha_bounds_e
    ) * enc_kw_edge.pop("alpha_scale", 1.0)

    if pos_cloned is not None:
        pass
    elif cloned_node_layout_kwargs:
        pos_cloned = layout_func_resolved(
            nt, group_by, sort_by, **cloned_node_layout_kwargs
        )

    if pos_cloned is not None:
        backend_obj.draw_nodes(
            axes, nt, pos_cloned, node_color, alpha, size, encodings_kwargs=enc_kw
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


def base_chord(
    G: nx.Graph,
    group_by: Hashable,
    weight_by: Hashable = None,
    sort_by: Hashable = None,
    node_palette: Optional[Union[Dict, List]] = None,
    edge_palette: Optional[Union[Dict, List]] = None,
    alpha: float = 0.4,
    radius: float = 10.0,
    backend: str = "matplotlib",
):
    """Chord diagram plotting function.

    Aggregates nodes into arc segments and edges into ribbons showing
    aggregate flow between groups.

    Parameters
    ----------
    G : nx.Graph
        A NetworkX Graph.
    group_by : Hashable
        Node metadata attribute key to group nodes. Required.
    weight_by : Hashable, optional
        Edge metadata attribute key for flow weight.
        If None, edges are counted.
    sort_by : Hashable, optional
        Node metadata attribute key to sort groups.
    node_palette : optional
        Custom color palette for groups.
    edge_palette : optional
        Unused, kept for API consistency.
    alpha : float
        Transparency for ribbons (default 0.4).
    radius : float
        Circle radius (default 10.0).
    backend : str
        Rendering backend ("matplotlib" or "plotly").
    """
    from nxviz.chord_compute import aggregate_edges, group_arcs, ribbon_coords
    from nxviz.utils import edge_table, node_table

    if group_by is None:
        raise TypeError(
            "group_by is required for chord diagrams. "
            "Provide a node attribute key to group nodes by."
        )

    nt = node_table(G)
    arcs = group_arcs(nt, group_by, palette=node_palette)

    et = edge_table(G)
    agg = aggregate_edges(et, nt, group_by, weight_by)

    ribbons = ribbon_coords(agg, arcs, radius=radius, alpha=alpha)

    if backend != "matplotlib":
        from nxviz.backend import get_backend

        backend_obj = get_backend(backend)
        axes = backend_obj.create_axes()
        backend_obj.draw_ribbons(axes, ribbons, **{})
        backend_obj.draw_arcs(axes, arcs, radius)
        backend_obj.draw_arc_labels(axes, arcs, radius)
        backend_obj.despine(axes)
        backend_obj.set_aspect_equal(axes)

        pos_data = {}
        for _, row in arcs.iterrows():
            mid_angle = (row["start_angle"] + row["end_angle"]) / 2
            x, y = to_cartesian(radius, mid_angle)
            pos_data[row["group"]] = np.array([x, y])
        backend_obj.rescale(axes, pos_data)

        fig = backend_obj.get_figure(axes)

        return fig

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for ribbon in ribbons:
        coords = ribbon["path_coords"]
        if len(coords) < 3:
            continue
        poly = plt.Polygon(
            coords,
            closed=True,
            facecolor=ribbon["color"],
            edgecolor=ribbon["color"],
            alpha=ribbon["alpha"],
            linewidth=0,
            zorder=1,
        )
        ax.add_patch(poly)

    arc_half = 0.025 * radius

    for _, row in arcs.iterrows():
        n_pts = max(int((row["end_angle"] - row["start_angle"]) * 50), 10)
        thetas = np.linspace(row["start_angle"], row["end_angle"], n_pts)
        outer_x = (radius + arc_half) * np.cos(thetas)
        outer_y = (radius + arc_half) * np.sin(thetas)
        inner_x = (radius - arc_half) * np.cos(thetas[::-1])
        inner_y = (radius - arc_half) * np.sin(thetas[::-1])
        verts_x = np.concatenate([outer_x, inner_x])
        verts_y = np.concatenate([outer_y, inner_y])
        verts = np.column_stack([verts_x, verts_y])
        poly = plt.Polygon(
            verts,
            closed=True,
            facecolor=row["color"],
            edgecolor=row["color"],
            linewidth=0.5,
            zorder=2,
        )
        ax.add_patch(poly)

    label_radius = radius + arc_half + radius * 0.08
    for _, row in arcs.iterrows():
        mid_angle = (row["start_angle"] + row["end_angle"]) / 2
        x, y = to_cartesian(label_radius, mid_angle)
        angle_deg = np.rad2deg(mid_angle)
        if 90 < angle_deg <= 270:
            rotation = angle_deg - 180
            ha = "right"
        else:
            rotation = angle_deg
            ha = "left"
        ax.text(
            x,
            y,
            str(row["group"]),
            ha=ha,
            va="center",
            rotation=rotation,
            rotation_mode="anchor",
            fontsize=10,
            zorder=3,
        )

    ax.set_aspect("equal")
    despine(ax)
    ax.relim()
    ax.autoscale_view()

    return ax


chord = partial(
    base_chord,
    group_by=None,
)
update_wrapper(chord, base_chord)
chord.__name__ = "api.chord"


def chord_hover_html(fig, height: str = "600px") -> str:
    """Return full HTML with hover-enabled ribbon highlighting for a Plotly chord figure.

    In marimo notebooks::

        fig = nv.chord(G, group_by="continent", weight_by="flow", backend="plotly")
        mo.iframe(nv.chord_hover_html(fig), height="600px")

    Args:
        fig: A ``go.Figure`` returned by ``chord(..., backend="plotly")``.
        height: iframe height string (default ``"600px"``).
    """
    import json
    import uuid

    from plotly.io import to_json

    fig_json = json.loads(to_json(fig))

    ribbon_meta = {}
    for i, trace in enumerate(fig.data):
        if getattr(trace, "name", None) == "ribbons" and getattr(trace, "meta", None):
            ribbon_meta[str(i)] = trace.meta

    if not ribbon_meta:
        return fig.to_html(include_plotlyjs="cdn")

    div_id = f"chord-{uuid.uuid4().hex[:8]}"
    data_json = json.dumps(fig_json["data"])
    layout_json = json.dumps(fig_json["layout"])
    config_json = json.dumps({"responsive": True})
    meta_json = json.dumps(ribbon_meta)

    js = (
        f"Plotly.newPlot('{div_id}', {data_json}, {layout_json}, {config_json})"
        f".then(function() {{"
        f"  var el = document.getElementById('{div_id}');"
        f"  var meta = {meta_json};"
        f"  var idx = Object.keys(meta);"
        f"  el.on('plotly_hover', function(ev) {{"
        f"    var h = ev.points[0].curveNumber;"
        f"    idx.forEach(function(i) {{"
        f"      var m = meta[i];"
        f"      var n = parseInt(i);"
        f"      if (n === h) {{"
        f"        Plotly.restyle(el, {{fillcolor: m.highlight_fill, 'line.color': m.highlight_line}}, [n]);"
        f"      }} else {{"
        f"        Plotly.restyle(el, {{fillcolor: m.dimmed_fill, 'line.color': m.dimmed_line}}, [n]);"
        f"      }}"
        f"    }});"
        f"  }});"
        f"  el.on('plotly_unhover', function() {{"
        f"    idx.forEach(function(i) {{"
        f"      var m = meta[i];"
        f"      Plotly.restyle(el, {{fillcolor: m.default_fill, 'line.color': m.default_line}}, [parseInt(i)]);"
        f"    }});"
        f"  }});"
        f"}});"
    )

    plotly_src = "https://cdn.plot.ly/plotly-latest.min.js"

    return (
        f"<!DOCTYPE html>\n"
        f"<html><head><script src='{plotly_src}'></script></head>\n"
        f"<body><div id='{div_id}'></div>\n"
        f"<script>{js}</script></body></html>"
    )


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
