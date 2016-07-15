from matplotlib.pyplot import plt


class BasePlot(object):
    """BasePlot: the base plotting object that computes the layouts."""
    def __init__(self, nodes, edges,
                 nodecolors, edgecolors,
                 nodeprops, edgeprops):
        super(BasePlot, self).__init__()
        self.nodes = nodes
        self.edges = edges

        self.set_nodeprops(nodeprops)
        self.set_edgeprops(edgeprops)
        self.set_nodecolors(nodecolors)
        self.set_edgecolors(edgecolors)

        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(1, 1, 1)

    def set_nodeprops(self, nodeprops):
        """
        Sets the node properties.
        """
        if nodeprops is not None:
            if isinstance(nodeprops, dict):
                self.nodeprops = nodeprops
            else:
                raise TypeError("nodeprops must be a dictionary")
        else:
            self.nodeprops = {}

    def set_edgeprops(self, edgeprops):
        """
        Sets the edge visualization properties.
        """
        if edgeprops is not None:
            if isinstance(edgeprops, dict):
                self.edgeprops = edgeprops
            else:
                raise TypeError("edgeprops must be a dictionary")
        else:
            self.edgeprops = {}

    def set_nodecolors(self, nodecolors):
        """
        Sets the nodecolors. Priority: nodecolor > nodeprops > default.

        By default, node color is blue.
        """
        if nodecolors is not None:
            self.nodecolors = nodecolors
        elif self.nodeprops:
            try:
                self.nodecolors = self.nodeprops.pop('facecolor')
            except KeyError:
                self.nodecolors = 'blue'
        else:
            self.nodecolors = 'blue'

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

    def draw_nodes(self):
        """
        Needs to be implemented for each plot.
        """
        pass

    def draw_edges(self):
        """
        Needs to be implemented for each plot.
        """
        pass

    def clone_axis(self):
        """
        Needs to be implemented for each plot, but only as necessary.

        Intent: Visually clone a selected axis on the plot to visualize
        within-group connectivity.
        """
        pass
