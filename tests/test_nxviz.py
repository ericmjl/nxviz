from nxviz.plots import BasePlot
import networkx as nx


def test_initialization():
    """
    Tests initialization of plot object.
    """
    n_nodes = 10
    G = nx.erdos_renyi_graph(n=n_nodes, p=0.3)

    b = BasePlot(graph=G)

    assert len(b.nodes) == len(G.nodes())


def make_graph_for_grouping():

    nodelist = [('Andrew', {'affiliation': 'MIT', 'year': 5}),
                ('Felipe', {'affiliation': 'Broad', 'year': 4}),
                ('Thomas', {'affiliation': 'Harvard', 'year': 2}),
                ('Elizabeth', {'affiliation': 'Broad', 'year': 3}),
                ('Lily', {'affiliation': 'MIT', 'year': 2}),
                ('Jessica', {'affiliation': 'MIT', 'year': 2})
                ]

    G = nx.Graph()
    G.add_nodes_from(nodelist)
    return G


def test_init_group_nodes():
    """
    Tests initialization with grouping of nodes.

    This only tests that the nodes are ordered correctly when sorted on the
    `node_grouping` key.
    """

    G = make_graph_for_grouping()
    b = BasePlot(graph=G, node_grouping='affiliation')

    assert b.nodes == [n for n, d in
                       sorted(G.nodes(data=True),
                              key=lambda x: x[1]['affiliation']
                              )
                       ]


def test_init_sort_and_group_nodes():
    """
    Tests initialization with sorting and grouping of nodes.

    This tests that the nodes are ordered correctly when first grouped on the
    `node_grouping` key, and then sorted within each group on the `node_order`
    key.
    """
    G = make_graph_for_grouping()

    b = BasePlot(graph=G, node_grouping='affiliation', node_order='year')

    assert b.nodes == [n for n, d in
                       sorted(G.nodes(data=True),
                              key=lambda x: (x[1]['affiliation'],
                                             x[1]['year'])
                              )
                       ]


def test_init_sort_nodes():
    """
    Tests initialization with sorting of nodes.

    This tests that the nodes are ordered correctly when sorted on the
    "node_order" key.
    """

    G = make_graph_for_grouping()

    b = BasePlot(graph=G, node_order='year')

    assert b.nodes == [n for n, d in
                       sorted(G.nodes(data=True),
                              key=lambda x: x[1]['year']
                              )
                       ]
