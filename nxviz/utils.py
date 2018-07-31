from collections import Counter

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
    assert is_data_homogenous(
        data_container
    ), "Data are not of a homogenous type!"

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


def to_pandas_nodes(G):  # noqa: N803
    """
    Convert nodes in the graph into a pandas DataFrame.
    """
    data = []
    for n, meta in G.nodes(data=True):
        d = dict()
        d['node'] = n
        d.update(meta)
        data.append(d)
    return pd.DataFrame(data)


def to_pandas_edges(G, x_kw, y_kw, **kwargs):  # noqa: N803
    """
    Convert Graph edges to pandas DataFrame that's readable to Altair.
    """
    # Get all attributes in nodes
    attributes = ['source', 'target', 'x', 'y', 'edge', 'pair']
    for e in G.edges():
        attributes += list(G.edges[e].keys())
    attributes = list(set(attributes))

    # Build a dataframe for all edges and their attributes
    df = pd.DataFrame(
        index=range(G.size()*2),
        columns=attributes
    )

    # Add node data to dataframe.
    for i, (n1, n2, d) in enumerate(G.edges(data=True)):
        idx = i*2
        x = G.node[n1][x_kw]
        y = G.node[n1][y_kw]
        data1 = dict(
            edge=i,
            source=n1,
            target=n2,
            pair=(n1, n2),
            x=x,
            y=y,
            **d
        )

        data2 = dict(
            edge=i,
            source=n1,
            target=n2,
            pair=(n1, n2),
            x=x,
            y=y,
            **d
        )

        df.loc[idx] = data1
        df.loc[idx+1] = data2

    return df
