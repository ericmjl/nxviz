"""Utility functions."""
from collections import Counter

import pandas as pd
import warnings
from typing import Iterable


def is_data_homogenous(data_container: Iterable):
    """
    Checks that all of the data in the container are of the same Python data
    type. This function is called in every other function below, and as such
    need not necessarily be called.

    :param data_container: A generic container of data points.
    """
    data_types = set([type(i) for i in data_container])
    return len(data_types) == 1


def infer_data_type(data_container: Iterable):
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

    - dtype = float:
        - min < 0 and max > 0: divergent
        - otherwise: continuous
    - dtype = integer:
        - greater than 12 distinct integers: continuous
        - otherwise: ordinal
    - dtype = object: categorical
    """
    if data.dtype == float:
        if data.min() < 0 and data.max() > 0:
            return "divergent"
        return "continuous"
    if data.dtype == int:
        if len(set(data)) > 9:
            return "continuous"
        return "ordinal"
    return "categorical"


def is_data_diverging(data_container: Iterable):
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


def is_groupable(data_container: Iterable):
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


def num_discrete_groups(data_container: Iterable):
    """
    Returns the number of discrete groups present in a data container.

    :param data_container: A generic container of data points.
    :type data_container: `iterable`
    """
    return len(set(data_container))


def items_in_groups(data_container: Iterable):
    """
    Returns discrete groups present in a data container and the number items
    per group.

    :param data_container: A generic container of data points.
    :type data_container: `iterable`
    """
    return Counter(data_container)


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


import networkx as nx


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
        if not G.is_directed():
            u, v = v, u
            row = dict()
            row.update(d)
            row["source"] = u
            row["target"] = v
            data.append(row)
    return pd.DataFrame(data)


from typing import Hashable, Iterable


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


def nonzero_sign(xy):
    """
    A sign function that won't return 0
    """
    return -1 if xy < 0 else 1
