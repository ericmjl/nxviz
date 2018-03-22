import networkx as nx

from nxviz.plots import BasePlot


def test_initialization():
    """
    Tests initialization of plot object.
    """
    n_nodes = 10
    G = nx.erdos_renyi_graph(n=n_nodes, p=0.3)  # noqa

    b = BasePlot(graph=G)

    assert len(b.nodes) == len(G.nodes())


def make_graph_for_grouping():

    nodelist = [('Andrew', {'affiliation': 'MIT', 'year': 5, 'score': -2.0}),
                ('Felipe', {'affiliation': 'Broad', 'year': 4, 'score': 0.0}),
                ('Tom', {'affiliation': 'Harvard', 'year': 2, 'score': 1.0}),
                ('Liz', {'affiliation': 'Broad', 'year': 3, 'score': 2.0}),
                ('Lily', {'affiliation': 'MIT', 'year': 2, 'score': 3.0}),
                ('Jessica', {'affiliation': 'MIT', 'year': 2, 'score': 0.0})
                ]

    G = nx.Graph()  # noqa
    G.add_nodes_from(nodelist)
    return G


def make_graph_for_edges():

    nodelist = [('a'),
                ('b'),
                ('c'),
                ('d'),
                ('e'),
                ('f')
                ]
    edgelist = [('a', 'b', {'weight': 0.1}),
                ('a', 'c', {'weight': 0.2}),
                ('b', 'd', {'weight': 0.6}),
                ('c', 'd', {'weight': 0.7}),
                ('e', 'd', {'weight': 0.8}),
                ('e', 'f', {'weight': 1.0}),
                ]

    G = nx.Graph()  # noqa
    G.add_nodes_from(nodelist)
    G.add_edges_from(edgelist)
    return G


def test_init_group_nodes():
    """
    Tests initialization with grouping of nodes.

    This only tests that the nodes are ordered correctly when sorted on the
    `node_grouping` key.
    """

    G = make_graph_for_grouping()  # noqa
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
    G = make_graph_for_grouping()   # noqa

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

    G = make_graph_for_grouping()  # noqa

    b = BasePlot(graph=G, node_order='year')

    assert b.nodes == [n for n, d in
                       sorted(G.nodes(data=True),
                              key=lambda x: x[1]['year']
                              )
                       ]


def test_init_data_types():
    """
    Checks that the data_types dictionary is initialized correctly.
    """

    G = make_graph_for_grouping()   # noqa

    b = BasePlot(graph=G, data_types={'year': 'ordinal',
                                      'affiliation': 'categorical'})
    assert isinstance(b.data_types, dict)


def test_init_node_colors():
    """
    Does two checks:
    1. If node_color is not passed in as a keyword argument, check that
       self.node_colors is a list of 'blue', of length (number of nodes).
    2. If node_color is passed in as a keyword argument, check that
       self.node_colors is a list with more than one element.
    """
    G = make_graph_for_grouping()  # noqa
    b = BasePlot(graph=G, node_color="year")
    assert len(set(b.node_colors)) > 1

    G = make_graph_for_grouping()  # noqa
    b = BasePlot(graph=G)
    assert len(set(b.node_colors)) == 1


def test_init_edge_colors():
    """
    Does two checks:
    1. If edge_color is passed in as a keyword argument, check that
       self.edge_colors is a list with more than one element.
    2. If edge_color is not passed in as a keyword argument, check that
       self.edge_colors is a list of 'black', of length 0.
    """
    G = make_graph_for_edges()  # noqa
    b = BasePlot(graph=G, edge_color="weight")
    assert len(set(b.edge_colors)) > 1

    G = make_graph_for_grouping()  # noqa
    b = BasePlot(graph=G)
    assert len(set(b.edge_colors)) == 0
