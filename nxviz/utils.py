from collections import Counter

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sns
from matplotlib.colors import ListedColormap
from palettable.colorbrewer import diverging, qualitative, sequential


def is_data_homogenous(data_container):
    """
    Checks that all of the data in the container are of the same Python data
    type. This function is called in every other function below, and as such
    need not necessarily be called.

    :param data_container: A generic container of data points.
    :type data_container: `iterable`
    """
    data_types = set([type(i) for i in data_container])
    return len(data_types) == 1


def infer_data_type(data_container):
    """
    For a given container of data, infer the type of data as one of
    continuous, categorical, or ordinal.

    For now, it is a one-to-one mapping as such:

    - str:   categorical
    - int:   ordinal
    - float: continuous

    There may be better ways that are not currently implemented below. For
    example, with a list of numbers, we can check whether the number of unique
    entries is less than or equal to 12, but has over 10000+ entries. This
    would be a good candidate for floats being categorical.

    :param data_container: A generic container of data points.
    :type data_container: `iterable`

    """
    warnings.warn(
        "`infer_data_type` is deprecated! " "Please use `infer_data_family` instead!"
    )
    # Defensive programming checks.
    # 0. Ensure that we are dealing with lists or tuples, and nothing else.
    assert isinstance(data_container, list) or isinstance(
        data_container, tuple
    ), "data_container should be a list or tuple."
    # 1. Don't want to deal with only single values.
    assert (
        len(set(data_container)) > 1
    ), "There should be more than one value in the data container."
    # 2. Don't want to deal with mixed data.
    assert is_data_homogenous(data_container), "Data are not of a homogenous type!"

    # Once we check that the data type of the container is homogenous, we only
    # need to check the first element in the data container for its type.
    datum = data_container[0]

    # Return statements below
    # treat binomial data as categorical
    # TODO: make tests for this.
    if len(set(data_container)) == 2:
        return "categorical"

    elif isinstance(datum, str):
        return "categorical"

    elif isinstance(datum, int):
        return "ordinal"

    elif isinstance(datum, float):
        return "continuous"

    else:
        raise ValueError("Not possible to tell what the data type is.")


def infer_data_family(data: pd.Series):
    """Infer data family from a column of data.

    The three families are "continuous", "ordinal", and "categorical".

    The rules:

    - dtype = float: continuous
    - dtype = integer:
        - greater than 12 distinct integers: continuous
        - otherwise: ordinal
    - dtype = object: categorical
    """
    if data.dtype == float:
        return "continuous"
    if data.dtype == int:
        if len(set(data)) > 9:
            return "continuous"
        else:
            return "ordinal"
    else:
        return "categorical"


def is_data_diverging(data_container):
    """
    We want to use this to check whether the data are diverging or not.

    This is a simple check, can be made much more sophisticated.

    :param data_container: A generic container of data points.
    :type data_container: `iterable`
    """
    assert infer_data_type(data_container) in [
        "ordinal",
        "continuous",
    ], "Data type should be ordinal or continuous"

    # Check whether the data contains negative and positive values.
    has_negative = False
    has_positive = False
    for i in data_container:
        if i < 0:
            has_negative = True
        elif i > 0:
            has_positive = True
    if has_negative and has_positive:
        return True
    else:
        return False


def is_groupable(data_container):
    """
    Returns whether the data container is a "groupable" container or not.

    By "groupable", we mean it is a 'categorical' or 'ordinal' variable.

    :param data_container: A generic container of data points.
    :type data_container: `iterable`
    """
    is_groupable = False
    if infer_data_type(data_container) in ["categorical", "ordinal"]:
        is_groupable = True
    return is_groupable


def num_discrete_groups(data_container):
    """
    Returns the number of discrete groups present in a data container.

    :param data_container: A generic container of data points.
    :type data_container: `iterable`
    """
    return len(set(data_container))


def items_in_groups(data_container):
    """
    Returns discrete groups present in a data container and the number items
    per group.

    :param data_container: A generic container of data points.
    :type data_container: `iterable`
    """
    return Counter(data_container)


def n_group_colorpallet(n):
    """If more then 8 categorical groups of nodes or edges this function
    creats the matching color_palette
    """
    cmap = ListedColormap(sns.color_palette("hls", n))
    return cmap


cmaps = {
    "Accent_2": qualitative.Accent_3,
    "Accent_3": qualitative.Accent_3,
    "Accent_4": qualitative.Accent_4,
    "Accent_5": qualitative.Accent_5,
    "Accent_6": qualitative.Accent_6,
    "Accent_7": qualitative.Accent_7,
    "Accent_8": qualitative.Accent_8,
    "continuous": sequential.YlGnBu_9,
    "diverging": diverging.RdBu_11,
    "weights": sns.cubehelix_palette(
        50, hue=0.05, rot=0, light=0.9, dark=0, as_cmap=True
    ),
}

import warnings


def to_pandas_nodes(G):  # noqa: N803
    """
    Convert nodes in the graph into a pandas DataFrame.
    """
    warnings.warn(
        "The function `to_pandas_nodes` is deprecated. "
        "Please use the `node_table` function instead."
    )
    data = []
    for n, meta in G.nodes(data=True):
        d = dict()
        d["node"] = n
        d.update(meta)
        data.append(d)
    return pd.DataFrame(data)


def node_table(G, group_by=None, sort_by=None):
    """Return the node table of a graph G.

    ## Parameters

    - `G`: A NetworkX graph.
    - `group_by`: A key in the node attribute dictionary.
    - `sort_by`: A key in the node attribute dictionary.

    ## Returns

    A pandas DataFrame, such that the index is the node
    and the columns are node attributes.
    """
    node_table = []
    node_index = []
    for n, d in G.nodes(data=True):
        node_table.append(d)
        node_index.append(n)
    df = pd.DataFrame(data=node_table, index=node_index)
    df = group_and_sort(df, group_by, sort_by)
    return df


def edge_table(G) -> pd.DataFrame:
    """Return the edge table of a graph.

    The nodes involved in the edge are keyed
    under the `source` and `target` keys.
    This is a requirement for use with the hammer_bundle module
    in datashader's bundler.

    The rest of their node attributes are returned as columns.
    """
    data = []
    for u, v, d in G.edges(data=True):
        row = dict()
        row.update(d)
        row["source"] = u
        row["target"] = v
        data.append(row)
    return pd.DataFrame(data)


from typing import Hashable


def group_and_sort(
    node_table: pd.DataFrame, group_by: Hashable = None, sort_by: Hashable = None
) -> pd.DataFrame:
    """Group and sort a node table."""
    sort_criteria = []
    if group_by:
        sort_criteria.append(group_by)
    if sort_by:
        sort_criteria.append(sort_by)
    if sort_criteria:
        node_table = node_table.sort_values(sort_criteria)
    return node_table


def to_pandas_edges(G, x_kw, y_kw, **kwargs):  # noqa: N803
    """
    Convert Graph edges to pandas DataFrame that's readable to Altair.
    """
    # Get all attributes in nodes
    attributes = ["source", "target", "x", "y", "edge", "pair"]
    for e in G.edges():
        attributes += list(G.edges[e].keys())
    attributes = list(set(attributes))

    # Build a dataframe for all edges and their attributes
    df = pd.DataFrame(index=range(G.size() * 2), columns=attributes)

    # Add node data to dataframe.
    for i, (n1, n2, d) in enumerate(G.edges(data=True)):
        idx = i * 2
        x = G.node[n1][x_kw]
        y = G.node[n1][y_kw]
        data1 = dict(edge=i, source=n1, target=n2, pair=(n1, n2), x=x, y=y, **d)

        data2 = dict(edge=i, source=n1, target=n2, pair=(n1, n2), x=x, y=y, **d)

        df.loc[idx] = data1
        df.loc[idx + 1] = data2

    return df
