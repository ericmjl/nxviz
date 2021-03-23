from nxviz.utils import node_table
from . import layouts, colors
import numpy as np
import networkx as nx
from copy import deepcopy


default_node_kwargs = {"node_size": 10}


def update_node_kwargs(node_kwargs):
    nodekw = deepcopy(default_node_kwargs)
    nodekw.update(node_kwargs)
    return nodekw


import pandas as pd
from typing import Hashable


def node_colors(nt: pd.DataFrame, color_by: Hashable):
    node_color = "black"
    if color_by:
        node_color = colors.data_color(nt[color_by])
    return node_color


def hive(
    G,
    group_by,
    sort_by=None,
    color_by=None,
    clone=False,
    layout_kwargs={},
    node_kwargs={},
    ax=None,
):
    nt = node_table(G)
    pos = layouts.hive(nt, group_by, sort_by, **layout_kwargs)
    pos_cloned = pos
    if clone:
        pos_cloned = layouts.hive(
            nt, group_by, sort_by, rotation=np.pi / 6, **layout_kwargs
        )

    node_color = node_colors(nt, color_by)
    nodekw = update_node_kwargs(node_kwargs)

    nx.draw_networkx_nodes(G, pos, node_color=node_color, **nodekw, ax=ax)
    nx.draw_networkx_nodes(G, pos_cloned, node_color=node_color, **nodekw, ax=ax)
    return pos, pos_cloned


def arc(G, group_by=None, sort_by=None, color_by=None, node_kwargs={}, ax=None):
    nt = node_table(G)
    pos = layouts.arc(nt, group_by, sort_by)
    node_color = node_colors(nt, color_by)
    nodekw = update_node_kwargs(node_kwargs)

    nx.draw_networkx_nodes(G, pos=pos, node_color=node_color, **nodekw, ax=ax)
    return pos


def circos(
    G, group_by=None, sort_by=None, color_by=None, radius=10, node_kwargs={}, ax=None
):
    nt = node_table(G)
    pos = layouts.circos(nt, group_by=group_by, sort_by=sort_by, radius=radius)
    node_color = node_colors(nt, color_by)

    nodekw = update_node_kwargs(node_kwargs)
    nx.draw_networkx_nodes(G, pos=pos, node_color=node_color, **nodekw, ax=ax)
    return pos


def parallel(G, group_by, sort_by=None, color_by=None, node_kwargs={}, ax=None):
    nt = node_table(G)
    pos = layouts.parallel(nt, group_by=group_by, sort_by=sort_by)
    node_color = node_colors(nt, color_by)

    nodekw = update_node_kwargs(node_kwargs)
    nx.draw_networkx_nodes(G, pos=pos, node_color=node_color, **nodekw, ax=ax)
    return pos
