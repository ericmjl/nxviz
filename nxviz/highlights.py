"""Highlights onto a particular graph."""

from typing import Callable, Hashable

from networkx.drawing import layout
from nxviz import layouts, lines, utils
from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt
from functools import partial, update_wrapper
import numpy as np
import pandas as pd
from copy import deepcopy

import networkx as nx


def node(
    G,
    node,
    layout_func,
    group_by,
    sort_by=None,
    # visual properties
    color="red",  # color
    radius=1,  # size
    alpha=1.0,  # transparency
    clone=False,
    cloned_node_layout_kwargs={},
):
    """Highlight one particular node."""
    nt = utils.node_table(G, group_by=group_by, sort_by=sort_by)
    pos = layout_func(nt, group_by=group_by, sort_by=sort_by)
    ax = plt.gca()
    zorder = max([_.zorder for _ in ax.get_children()])
    c = Circle(xy=pos[node], fc=color, radius=radius, zorder=zorder)
    ax.add_patch(c)
    if clone:
        pos_cloned = layout_func(
            nt, group_by=group_by, sort_by=sort_by, **cloned_node_layout_kwargs
        )
        c = Circle(xy=pos_cloned[node], fc=color, radius=radius, zorder=zorder + 1)
        ax.add_patch(c)


circos_node = partial(node, layout_func=layouts.circos, group_by=None)
update_wrapper(circos_node, node)
circos_node.__name__ = "highlights.circos_node"
parallel_node = partial(node, layout_func=layouts.parallel, group_by=None)
update_wrapper(parallel_node, node)
parallel_node.__name__ = "highlights.parallel_node"

arc_node = partial(node, layout_func=layouts.arc, group_by=None)
update_wrapper(arc_node, node)
arc_node.__name__ = "highlights.arc_node"


hive_node = partial(
    node,
    layout_func=layouts.hive,
    clone=True,
    cloned_node_layout_kwargs={"rotation": np.pi / 6},
)
update_wrapper(hive_node, node)
hive_node.__name__ = "highlights.hive_node"
matrix_node = partial(
    node,
    layout_func=layouts.matrix,
    group_by=None,
    clone=True,
    cloned_node_layout_kwargs={"axis": "y"},
)
update_wrapper(matrix_node, node)
matrix_node.__name__ = "highlights.matrix_node"


def edge(
    G,
    source,
    target,
    layout_func,
    line_func,
    group_by,
    sort_by,
    color="red",  # color
    lw=1.0,  # size
    alpha=1.0,  # transparency
    clone=False,
    cloned_node_layout_kwargs={},
    line_func_aes_kw={"zorder": 30, "fc": "none"},
    line_func_kwargs={},
):
    """Highlight one particular edge."""
    nt = utils.node_table(G, group_by=group_by, sort_by=sort_by)
    et = utils.edge_table(G).query("source == @source").query("target == @target")
    pos = layout_func(nt, group_by=group_by, sort_by=sort_by)

    line_func_kwargs = deepcopy(line_func_kwargs)
    line_func_kwargs.update(
        et=et,
        pos=pos,
        edge_color=pd.Series([color], index=et.index),
        alpha=pd.Series([alpha], index=et.index),
        lw=pd.Series([lw], index=et.index),
        aes_kw=line_func_aes_kw,
    )

    if clone:
        pos_cloned = layout_func(
            nt, group_by=group_by, sort_by=sort_by, **cloned_node_layout_kwargs
        )
        line_func_kwargs["pos_cloned"] = pos_cloned

    patches = line_func(**line_func_kwargs)
    ax = plt.gca()
    for patch in patches:
        ax.add_patch(patch)


circos_edge = partial(
    edge,
    layout_func=layouts.circos,
    line_func=lines.circos,
    group_by=None,
    sort_by=None,
)
update_wrapper(circos_edge, node)
circos_edge.__name__ = "highlights.circos_edge"

arc_edge = partial(
    edge,
    layout_func=layouts.arc,
    line_func=lines.arc,
    group_by=None,
    sort_by=None,
    line_func_aes_kw={"zorder": 1},
)
update_wrapper(arc_edge, node)
arc_edge.__name__ = "highlights.arc_edge"

hive_edge = partial(
    edge,
    layout_func=layouts.hive,
    line_func=lines.hive,
    sort_by=None,
    clone=True,
    cloned_node_layout_kwargs={"rotation": np.pi / 6},
)
update_wrapper(hive_edge, node)
hive_edge.__name__ = "highlights.hive_edge"


matrix_edge = partial(
    edge,
    layout_func=layouts.matrix,
    line_func=lines.matrix,
    group_by=None,
    sort_by=None,
    clone=True,
    cloned_node_layout_kwargs={"axis": "y"},
    line_func_aes_kw={},
)
update_wrapper(matrix_edge, node)
matrix_edge.__name__ = "highlights.matrix_edge"

parallel_edge = partial(
    edge,
    layout_func=layouts.parallel,
    line_func=lines.line,
    sort_by=None,
    line_func_aes_kw={"zorder": 1},
)
update_wrapper(parallel_edge, node)
parallel_edge.__name__ = "highlights.parallel_edge"


def matrix_row(
    G: nx.Graph,
    node: Hashable,
    group_by: Hashable = None,
    sort_by: Hashable = None,
    axis="x",
    color="red",
):
    """Highlight one row (or column) in the matrix plot."""
    nt = utils.node_table(G)
    pos = layouts.matrix(nt, group_by=group_by, sort_by=sort_by, axis=axis)
    x, y = pos[node]

    width = 2
    height = 2 * len(G)
    xy = x - 1, y + 1
    if axis == "y":
        width, height = height, width
        xy = x + 1, y - 1
    rectangle = Rectangle(
        xy=xy, width=width, height=height, fc=color, ec="none", alpha=0.3
    )
    ax = plt.gca()
    ax.add_patch(rectangle)
