"""Deprecated module no longer used."""
import pandas as pd
from networkx import Graph, MultiGraph


def graph_from_dataframe(
    dataframe,
    threshold_by_percent_unique=0.1,
    threshold_by_count_unique=None,
    node_id_columns=[],
    node_property_columns=[],
    edge_property_columns=[],
    node_type_key="type",
    edge_type_key="type",
    collapse_edges=True,
    edge_agg_key="weight",
):
    """
    Build an undirected graph from a pandas dataframe.

    This function attempts to infer which cells should become nodes
    based on either:

        a. what percentage of the column are unique values (defaults to 10%)
        b. an explicit count of unique values (i.e. any column with 7 unique
           values or less)
        c. an explicit list of column keys (i.e.
           ['employee_id', 'location_code'])

    Column headers are preserved as node and edge 'types'. By default, this is
    stored using the key 'type' which is used by some graph import processes
    but can be reconfigured.

    This function uses a MultiGraph structure during the build phase so that it
    is possible to make multiple connections between nodes. By default, at the
    end of the build phase, the MultiGraph is converted to a Graph and the
    count of edges between each node-pair is written as a 'weight' property.

    :param pandas.DataFrame dataframe: A pandas dataframe containing the data
        to be converted into a graph.
    :param float threshold_by_percent_unique: A percent value used to determine
        whether a column should be used to generate nodes based on its
        cardinality (i.e. in a dataframe with 100 rows, treat any column with
        10 or less unique values as a node)
    :param int threshold_by_count_unique: A numeric value used to determine
        whether a column should be used to generate nodes based on its
        cardinality (i.e. if 7 is supplied, treat any column with 7 or less
        unique values as a node) - supplying a value will take priority over
        percent_unique
    :param list node_id_columns: A list of column headers to use for generating
        nodes. Suppyling any value will take precedence over
        threshold_by_percent_unique or threshold_by_count_unique. Note: this
        can cause the size of the graph to expand significantly since every
        unique value in a column will become a node.
    :param list node_property_columns: A list of column headers to use for
        generating properties of nodes. These can include the same column
        headers used for the node id.
    :param list edge_property_columns: A list of column headers to use for
        generating properties of edges.
    :param str node_type_key: A string that sets the key will be used to
        preserve the column name as node property (this is useful for importing
        networkx graphs to databases that distinguish between node 'types' or
        for visually encoding those types in plots).
    :param str edge_type_key: A string that sets the key will be used to keep
        track of edge relationships an 'types' (this is useful for importing
        networkx graphs to databases that distinguish between edge'types' or
        for visually encoding those types in plots). Edge type values are
        automatically set to <node_a_id>_<node_b_id>.
    :param bool collapse_edges: Graphs are instantiated as a 'MultiGraph'
        (allow multiple edges between nodes) and then collapsed into a 'Graph'
        which only has a single edge between any two nodes. Information is
        preserved by aggregating the count of those edges as a 'weight' value.
        Set this value to False to return the MultiGraph. Note: this can cause
        the size of the graph to expand significantly since each row can
        potentially have n! edges where n is the number of columns in the
        dataframe.
    :param str edge_agg_key: A string that sets the key the edge count will be
        assigned to when edges are aggregated.
    :returns: A networkx Graph (or MultiGraph if collapse_edges is set to
        False).
    """

    assert isinstance(dataframe, pd.DataFrame), "{} is not a pandas DataFrame".format(
        dataframe
    )

    M = MultiGraph()

    # if explicit specification of node_id_columns is provided, use those
    if len(node_id_columns) > 0:
        node_columns = node_id_columns
    else:
        # otherwise, compute with thresholds based on the dataframe
        if threshold_by_count_unique:
            node_columns = sorted(
                [
                    col
                    for col in dataframe.columns
                    if dataframe[col].nunique() <= threshold_by_count_unique
                ]
            )
        else:
            node_columns = sorted(
                [
                    col
                    for col in dataframe.columns
                    if dataframe[col].nunique() / dataframe.shape[0]
                    <= threshold_by_percent_unique  # NOQA to preserve meaningful variable names
                ]
            )

    # use the unique values for each node column as node types
    for node_type in node_columns:
        M.add_nodes_from(
            [
                (node, {node_type_key: node_type})
                for node in dataframe[node_type].unique()
            ]
        )

    # iterate over the rows and generate an edge for each pair of node columns
    for i, row in dataframe.iterrows():
        # assemble the edge properties as a dictionary
        edge_properties = {k: row[k] for k in edge_property_columns}

        # iterate over the node_ids in each node_column of the dataframe row
        node_buffer = []
        for node_type in node_columns:
            node_id = row[node_type]

            # get a reference to the node and assign any specified properties
            node = M.nodes[node_id]
            for k in node_property_columns:
                # if values are not identical, append with a pipe delimiter
                if k not in node:
                    node[k] = row[k]
                elif isinstance(node[k], str) and str(row[k]) not in node[k]:
                    node[k] += "|{}".format(str(row[k]))
                elif str(row[k]) not in str(node[k]):
                    node[k] = str(node[k]) + "|{}".format(str(row[k]))

            # build edges using precomputed edge properties
            for other_node_id, other_node_type in node_buffer:
                # sort node_type so undirected edges all share the same type
                ordered_name = "_".join(sorted([node_type, other_node_type]))
                edge_properties[edge_type_key] = ordered_name
                M.add_edge(node_id, other_node_id, **edge_properties)

            # store the node from this column in the buffer for future edges
            node_buffer.append((node_id, node_type))

    if collapse_edges:
        # convert the MultiGraph to a Graph
        G = Graph(M)
        k = edge_agg_key
        # preserve the edge count as a sum of the weight values
        for u, v, data in M.edges(data=True):
            w = data[k] if k in data else 1.0
            edge = G[u][v]
            edge[k] = (w + edge[k]) if k in edge else w
        return G

    return M
