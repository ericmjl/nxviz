"""Highlights onto a particular graph."""

from nxviz import layouts, lines, utils
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from functools import partial
import numpy as np
import pandas as pd


def node(
    G,
    node,
    layout_func,
    group_by,
    sort_by=None,
    # Aesthetic properties
    color="red",  # color
    radius=1,  # size
    alpha=1.0,  # transparency
    clone=False,
    cloned_node_layout_kwargs={},
):
    """Highlight one particular node."""
    nt = utils.node_table(G, group_by=group_by, sort_by=sort_by)
    pos = layout_func(nt, group_by=group_by, sort_by=sort_by)
    c = Circle(xy=pos[node], fc=color, radius=radius, zorder=20)
    ax = plt.gca()
    ax.add_patch(c)
    if clone:
        pos_cloned = layout_func(
            nt, group_by=group_by, sort_by=sort_by, **cloned_node_layout_kwargs
        )
        c = Circle(xy=pos_cloned[node], fc=color, radius=radius, zorder=20)
        ax.add_patch(c)


circos_node = partial(node, layout_func=layouts.circos, group_by=None)
parallel_node = partial(node, layout_func=layouts.parallel, group_by=None)
arc_node = partial(node, layout_func=layouts.arc, group_by=None)


hive_node = partial(
    node,
    layout_func=layouts.hive,
    clone=True,
    cloned_node_layout_kwargs={"rotation": np.pi / 6},
)
matrix_node = partial(
    node,
    layout_func=layouts.matrix,
    group_by=None,
    clone=True,
    cloned_node_layout_kwargs={"axis": "y"},
)


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
    nt = utils.node_table(G, group_by=group_by, sort_by=sort_by)
    et = utils.edge_table(G).query("source == @source").query("target == @target")
    pos = layout_func(nt, group_by=group_by, sort_by=sort_by)

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

arc_edge = partial(
    edge,
    layout_func=layouts.arc,
    line_func=lines.arc,
    group_by=None,
    sort_by=None,
)

hive_edge = partial(
    edge,
    layout_func=layouts.hive,
    line_func=lines.hive,
    sort_by=None,
    clone=True,
    cloned_node_layout_kwargs={"rotation": np.pi / 6},
)

matrix_edge = partial(
    edge,
    layout_func=layouts.matrix,
    line_func=lines.matrix,
    group_by=None,
    sort_by=None,
    clone=True,
    cloned_node_layout_kwargs={"axis": "y"},
    line_func_kwargs={"directed": False},
)
