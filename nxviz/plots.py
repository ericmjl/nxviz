from .geometry import node_theta, get_cartesian
from collections import defaultdict
from matplotlib.path import Path

import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt


class BasePlot(object):
    """
    BasePlot: An extensible class for designing new network visualizations.

    The BasePlot constructor takes in a nodelist `nodes` and an edgelist
    `edges`. This design is intentional, rather than taking in a networkx
    graph (commonly referred to as `G` in their examples). Doing so allows
    for other graph representations to be fed in, such as sets of nodes and
    sets of edges.
    """
    def __init__(self, nodes, edges,
                 nodecolors='blue', edgecolors='black',
                 nodeprops=dict(radius=0.3), edgeprops=dict(alpha=0.5),
                 figsize=(8, 8)):
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

        # Set the Axes object splines to be invisible.
        for k in self.ax.spines.keys():
            self.ax.spines[k].set_visible(False)

    def set_nodeprops(self, nodeprops):
        """
        Sets the node properties. Follows matplotlib conventions.

        This provides a convenient way for applying a particular styling (e.g.
        border width, border dashes, alpha) to all nodes. Currently, only color
        is customizable by using the `set_nodecolors(iterable)` function.

        TODO: Add link to matplotlib conventions.
        """
        assert isinstance(nodeprops, dict),\
            "nodeprops must be a dictionary, even if empty"
        self.nodeprops = nodeprops

    def set_edgeprops(self, edgeprops):
        """
        Sets the edge visualization properties. Follows matplotlib conventions.

        TOOD: Add link to matplotlib conventions.
        """
        assert isinstance(edgeprops, dict),\
            "edgeprops must be a dictionary, even if empty"
        self.edgeprops = edgeprops

    def set_nodecolors(self, nodecolors):
        """
        Sets the nodecolors. Priority: nodecolor > nodeprops > default.

        `nodecolors` should be either a `string` or an iterable (list, tuple,
        dict).

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
        elif is_dict:
            assert set(nodecolors.keys()) == set(self.nodes),\
                "the all nodes in the graph must be present as keys in the " +\
                "dictionary"
        elif is_string:
            self.nodecolors = [nodecolors] * len(self.nodes)
        else:
            self.nodecolors = ['blue'] * len(self.nodes)

    def set_edgecolors(self, edgecolors):
        """
        Sets the edgecolors. Priority: edgecolor > edgeprops > default.

        `edgecolors` should be either a `string` or an iterable (list, tuple,
        dict).

        If `edgecolors` is a `string`, all edges will carry that color.

        If `edgecolors` is a `list` or `tuple`, then edges will be coloured in
        order by the list or tuple elements.

        If `edgecolors` is a `dict`, then the keys have to be all present in
        the edgelist.

        By default, edge color is black.
        """
        # Defensive check that nodecolors is an acceptable data type.
        is_string = isinstance(edgecolors, str)
        is_list = isinstance(edgecolors, list)
        is_tuple = isinstance(edgecolors, tuple)
        is_dict = isinstance(edgecolors, dict)
        assert is_string or is_tuple or is_list or is_dict,\
            "`edgecolors` must be a string, list, tuple, or dict"

        if is_list or is_tuple:
            assert len(edgecolors) == len(self.edges),\
              "`edgecolors` must be of the same length as the number of edges"
            self.edgecolors = edgecolors
        elif is_dict:
            assert set(edgecolors.keys()) == set(self.edges),\
                "the keys in edgecolors must be identical to the edges"
            self.edgecolors = edgecolors
        elif is_string:
            self.edgecolors = [edgecolors] * len(self.edges)
        else:
            self.edgecolors = ['black'] * len(self.edges)

        # if self.edgeprops:
        #     try:
        #         self.edgecolors = self.edgeprops.pop('edgecolors')
        #     except KeyError:
        #         self.edgecolors = ['black'] * len(self.edges)
        # else:
        #     self.edgecolors = ['black'] * len(self.edges)

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


class CircosPlot(BasePlot):
    """
    Plotting object for CircosPlot.
    """
    def __init__(self, nodes, edges, plot_radius,
                 nodecolors='blue', edgecolors='black',
                 nodeprops=dict(radius=0.3), edgeprops=dict(alpha=0.5),
                 figsize=(8, 8)):
        # Initialize using BasePlot
        BasePlot.__init__(self, nodes, edges)
        # The following attributes are specific to CircosPlot
        self.plot_radius = plot_radius
        # The rest of the relevant attributes are inherited from BasePlot.
        self.compute_node_positions()
        self.ax.set_xlim(-radius*1.2, radius*1.2)
        self.ax.set_ylim(-radius*1.2, radius*1.2)
        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)
        self.ax.set_aspect('equal')

    def compute_node_positions(self):
        """
        Uses the get_cartesian function to computes the positions of each node
        in the Circos plot.

        Returns `xs` and `ys`, lists of x- and y-coordinates.
        """
        xs = []
        ys = []
        for node in self.nodes:
            theta = node_theta(self.nodes, node)
            x, y = get_cartesian(self.plot_radius, theta)
            xs.append(x)
            ys.append(y)
        self.node_coords = {'x': xs, 'y': ys}

    def draw_nodes(self):
        """
        Renders nodes to the figure.
        """
        node_r = self.nodeprops['radius']
        for i, node in enumerate(self.nodes):
            x = self.node_coords['x'][i]
            y = self.node_coords['y'][i]
            self.nodeprops['facecolor'] = self.nodecolors[i]
            node_patch = patches.Ellipse((x, y), node_r, node_r,
                                         lw=0, **self.nodeprops)
            self.ax.add_patch(node_patch)

    def draw_edges(self):
        """
        Renders edges to the figure.
        """
        for i, (start, end) in enumerate(self.edges):
            start_theta = node_theta(self.nodes, start)
            end_theta = node_theta(self.nodes, end)
            verts = [get_cartesian(self.plot_radius, start_theta),
                     (0, 0),
                     get_cartesian(self.plot_radius, end_theta)]
            codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]

            path = Path(verts, codes)
            self.edgeprops['facecolor'] = 'none'
            self.edgeprops['edgecolor'] = self.edgecolors[i]
            patch = patches.PathPatch(path, lw=1, **self.edgeprops)
            self.ax.add_patch(patch)


class HivePlot(BasePlot):
    """
    Plotting object for HivePlot.
    """
    def __init__(self, nodes, edges,
                 nodecolors='blue', edgecolors='black',
                 nodeprops=dict(radius=0.2), edgeprops=dict(alpha=0.5),
                 figsize=(8, 8)):
        # Initialize using BasePlot
        BasePlot.__init__(self, nodes, edges)

        # The following method calls are specific to HivePlot.
        # 1. Set the .nodes attribute, but first do type checking.
        self.set_nodes(nodes)
        # 2. Set the major and minor angle attributes.
        self.set_major_angle()
        self.set_minor_angle()
        # 3. Set the nodecolors attributes.
        self.set_nodecolors(nodecolors)
        # 4. Compute node positions.
        self.compute_node_positions()
        # 5. Set the aspect ratio of the plot to be equal.
        self.ax.set_aspect('equal')
        # 6. Set the xlim and ylim of the plot.
        # Change the following two lines to an automatic function that computes
        # the appropriate x- and y- limits from the number of nodes in each
        # group.
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

    def set_xylims(self):
        pass

    def set_nodes(self, nodes):
        """
        Sets the nodes attribute.

        Checks that `nodes` is a dictionary where the key is the group ID and
        the value is a list of nodes that belong in that group.
        """
        assert isinstance(nodes, dict), 'nodes must be a dictionary'
        for k, v in nodes.items():
            assert isinstance(v, list) or isinstance(v, tuple),\
                'each value in the dictionary must be a list or tuple'
        assert len(nodes.keys()) in [2, 3], 'there can only be 2 or 3 groups'

        self.nodes = nodes

    def set_major_angle(self):
        """
        Sets the major angle between the plot groups, in radians.
        """
        self.major_angle = 2 * np.pi / len(self.nodes.keys())

    def set_minor_angle(self):
        """
        Sets the minor angle between the plot groups, in radians.
        """
        self.minor_angle = 2 * np.pi / 12

    def set_nodecolors(self, nodecolors):
        """
        Sets the nodecolors.

        `nodecolors` can be specified as either a single string, or as a
        dictionary of group_identifier:strings.

        Performs type checking to ensure that nodecolors is specified as a
        dictionary where the keys must match up with the .nodes attribute.

        Otherwise
        """
        assert isinstance(nodecolors, dict) or isinstance(nodecolors, str)
        if isinstance(nodecolors, dict):
            assert set(nodecolors.keys()) == set(self.nodes.keys())
            self.nodecolors = nodecolors
        elif isinstance(nodecolors, str):
            self.nodecolors = dict()
            for k in self.nodes.keys():
                self.nodecolors[k] = nodecolors

    def has_edge_within_group(self, group):
        """
        Checks whether there are within-group edges or not.
        """
        assert group in self.nodes.keys(),\
            "{0} not one of the group of nodes".format(group)
        nodelist = self.nodes[group]
        for n1, n2 in self.edges:
            if n1 in nodelist and n2 in nodelist:
                return True

    def compute_node_positions(self):
        """
        Computes the positions of each node on the plot.

        Sets the node_coords attribute inherited from BasePlot.
        """
        xs = defaultdict(lambda: defaultdict(list))
        ys = defaultdict(lambda: defaultdict(list))
        for g, (grp, nodes) in enumerate(self.nodes.items()):
            if self.has_edge_within_group(grp):
                for r, node in enumerate(nodes):
                    theta = g * self.major_angle - self.minor_angle
                    x, y = get_cartesian(r+2, theta)
                    xs[grp]['minus'].append(x)
                    ys[grp]['minus'].append(y)

                    theta = g * self.major_angle + self.minor_angle
                    x, y = get_cartesian(r+2, theta)
                    xs[grp]['plus'].append(x)
                    ys[grp]['plus'].append(y)
            else:
                for r, node in enumerate(nodes):
                    theta = g * self.major_angle
                    x, y = get_cartesian(r+2, theta)
                    xs[grp]['axis'].append(x)
                    ys[grp]['axis'].append(y)
        self.node_coords = dict(x=xs, y=ys)

    def draw_nodes(self):
        """
        Renders nodes to the figure.
        """
        for grp, nodes in self.nodes.items():
            for r, n in enumerate(nodes):
                if self.has_edge_within_group(grp):
                    x = self.node_coords['x'][grp]['minus'][r]
                    y = self.node_coords['y'][grp]['minus'][r]
                    self.draw_node(grp, x, y)

                    x = self.node_coords['x'][grp]['plus'][r]
                    y = self.node_coords['y'][grp]['plus'][r]
                    self.draw_node(grp, x, y)

                else:
                    x = self.node_coords['x'][grp]['axis'][r]
                    y = self.node_coords['y'][grp]['axis'][r]
                    self.draw_node(grp, x, y)

    def draw_node(self, group, x, y):
        """
        Convenience function for simplifying the code in draw_nodes().
        """
        circle = plt.Circle(xy=(x, y), radius=self.nodeprops['radius'],
                            color=self.nodecolors[group], linewidth=0)
        self.ax.add_patch(circle)

    def draw_edges(self):
        """
        Renders the edges to the figure.
        """
        pass

    def draw_edge(self, n1, n2):
        """

        """
        pass
