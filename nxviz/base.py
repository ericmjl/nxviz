import matplotlib.pyplot as plt


class BasePlot(object):
    """BasePlot: the base plotting object that computes the layouts."""
    def __init__(self, nodes, edges,
                 nodecolors='blue', edgecolors='black',
                 nodeprops=dict(), edgeprops=dict(),
                 figsize=None):
        super(BasePlot, self).__init__()
        self.nodes = nodes
        self.edges = edges

        # Set the node and edge props and colors.
        # These are written with functions because there are type checks that
        # have to take place first, and it would make the __init__ function
        # unwieldy to have them all in here.
        #
        # Later if we support other backends, such as Bokeh, it may be wise to
        # set these as "generic" parameters that we can write translators for
        # to other packages.
        self.set_nodeprops(nodeprops)
        self.set_edgeprops(edgeprops)
        self.set_nodecolors(nodecolors)
        self.set_edgecolors(edgecolors)
        # These functions end up setting the following object attributes:
        # - self.nodeprops
        # - self.edgeprops
        # - self.nodecolors
        # - self.edgecolors

        # Initialize a figure object with an axes subplot.
        # Later on if we support other backends, such as Bokeh, then it would
        # be wise to take this out of the class.
        self.figure = plt.figure(figsize=figsize)
        self.ax = self.figure.add_subplot(1, 1, 1)

        # We have an attribute that stores the x- and y-coordinates of each
        # node. They should be in the same order as self.nodes.
        self.node_coords = None

    def set_nodeprops(self, nodeprops):
        """
        Sets the node properties. Follows matplotlib conventions.

        This provides a convenient way for applying a particular styling (e.g.
        border width, border dashes, alpha) to all nodes. Currently, only color
        is customizable by using the `set_nodecolors(iterable)` function.

        TODO: Add link to matplotlib conventions.
        """
        assert isinstance(nodeprops, dict), "nodeprops must be a dictionary, even if empty"
        self.nodeprops = nodeprops

    def set_edgeprops(self, edgeprops):
        """
        Sets the edge visualization properties. Follows matplotlib conventions.

        TOOD: Add link to matplotlib conventions.
        """
        assert isinstance(edgeprops, dict), "edgeprops must be a dictionary, even if empty"
        self.edgeprops = edgeprops

    def set_nodecolors(self, nodecolors):
        """
        Sets the nodecolors. Priority: nodecolor > nodeprops > default.

        `nodecolors` should be either a `string` or an iterable (list, tuple, dict).

        If `nodecolors` is a `string`, all nodes will carry that color.

        If `nodecolors` is a `list` or `tuple`, then nodes will be coloured in
        order by the list or tuple elements.

        If `nodecolors` is a `dict`, then the keys have to be all present in
        the nodelist.

        By default, node color is blue.
        """
        # Defensive check that nodecolors is an acceptable data type.
        is_string = isinstance(nodecolors, str)
        is_list = isinstance(nodecolors, list)
        is_tuple = isinstance(nodecolors, tuple)
        is_dict = isinstance(nodecolors, dict)
        assert is_string or is_tuple or is_list or is_dict,\
            "`nodecolors` must be a string, list, tuple, or dict"

        # If `nodecolors` is an iterable, check that it is of the same length
        # as the number of nodes in the graph.
        if is_list or is_tuple:
            assert len(nodecolors) == len(self.nodes),\
                "`nodecolors` iterable must be the same length as nodes"
            self.nodecolors = nodecolors
        # Else, if nodes is a string, set `nodecolors` to be a list of the same
        # length as the number of nodes in the graph.
        graph_size = len(self.nodes)
        elif is_dict:
            assert set(nodecolors.keys()) == set(self.nodes),\
                "the all nodes in the graph must be present as keys in the " +\
                "dictionary"
        elif is_string:
            self.nodecolors = [nodecolors] * graph_size
        else:
            self.nodecolors = ['blue'] * graph_size

    def set_edgecolors(self, edgecolors):
        """
        Sets the edge colors. Priority: edgecolor > edgeprops > default.

        By default, edge color is black.
        """
        if edgecolors is not None:
            self.edgecolors = edgecolors
        elif self.edgeprops:
            try:
                self.edgecolors = self.edgeprops.pop('edgecolors')
            except KeyError:
                self.edgecolors = 'black'
        else:
            self.edgecolors = 'black'

    def draw(self):
        self.draw_nodes()
        self.draw_edges()

    def compute_node_positions(self):
        """
        Computes the positions of each node on the plot.

        Needs to be implemented for each plot.
        """
        pass

    def draw_nodes(self):
        """
        Renders the nodes to the plot or screen.

        Needs to be implemented for each plot.
        """
        pass

    def draw_edges(self):
        """
        Renders the nodes to the plot or screen.

        Needs to be implemented for each plot.
        """
        pass
