import pandas as pd
from networkx import Graph, MultiGraph


def graph_from_dataframe(
        dataframe,
        threshold_by_percent_unique=0.1,
        threshold_by_count_unique=None,
        node_id_columns=[],
        node_property_columns=[],
        edge_property_columns=[],
        collapse_edges=True,
        edge_agg_key='weight'):
    '''
    Build an undirected graph from a pandas dataframe.
    This function attempts to infer which cells should become nodes
    based on either:
        a) what percentage of the column are unique values (defaults to 10%)
        b) an explicit count of unique values
            (i.e. any column with 10 unique columns or less)
        c) an explicit list of column keys
            (i.e. ['employee_id', 'location_code'])
    '''
    assert isinstance(dataframe, pd.DataFrame), \
        "{} is not a pandas DataFrame".format(dataframe)

    M = MultiGraph()

    # if explicit specification of node_id_columns is provided, use those
    if len(node_id_columns) > 0:
        node_columns = node_id_columns
    else:
        # otherwise, compute with thresholds based on the dataframe
        if(threshold_by_count_unique):
            node_columns = sorted([
                    col for col in dataframe.columns
                    if dataframe[col].nunique() <= threshold_by_count_unique
                ])
        else:
            node_columns = sorted([
                    col for col in dataframe.columns if
                    dataframe[col].nunique() / dataframe.shape[0] <= threshold_by_percent_unique  # NOQA to preserve meaningful variable names
                ])

    # use the unique values for each node column as node types
    for node_type in node_columns:
        M.add_nodes_from([(node, {'type': node_type})
                          for node in dataframe[node_type].unique()])

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
                ordered_name = '_'.join(sorted([node_type, other_node_type]))
                edge_properties['type'] = ordered_name
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
