from .geometry import node_theta, get_cartesian, circos_radius
from collections import defaultdict
from matplotlib.path import Path

import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt


class BasePlot(object):
    """
    BasePlot: An extensible class for designing new network visualizations.

    The BasePlot constructor takes in a NetworkX graph object, and a series of
    keyword arguments specifying how nodes and edges should be styled and
    ordered.

    An optional data_types dictionary can be passed in to bypass data type
    inference.
    """
    def __init__(self, graph, node_order=None, node_size=None,
                 node_grouping=None, node_color=None, edge_width=None,
                 edge_color=None, data_types=None):
        super(BasePlot, self).__init__()
        # Set graph object
        self.graph = graph

        # Set node keys
        self.node_order = node_order
        self.node_size = node_size
        self.node_grouping = node_grouping
        self.node_color = node_color
        # Set edge keys
        self.edge_width = edge_width
        self.edge_color = edge_color

        # Set data_types dictionary
        if not data_types:
            self.data_types = dict()
        else:
            self.data_types = data_types

        # self.figure = plt.figure(figsize=figsize)
        # self.ax = self.figure.add_subplot(1, 1, 1)
        #
        # # Set the Axes object splines to be invisible.
        # for k in self.ax.spines.keys():
        #     self.ax.spines[k].set_visible(False)

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
    def __init__(self, graph, node_order=None, node_size=None,
                 node_grouping=None, node_color=None, edge_width=None,
                 edge_color=None, data_types=None):
        # Initialize using BasePlot
        BasePlot.__init__(self, graph, node_order=None, node_size=None,
                          node_grouping=None, node_color=None, edge_width=None,
                          edge_color=None, data_types=None)
        # The following attributes are specific to CircosPlot
        # self.plot_radius = plot_radius
        # The rest of the relevant attributes are inherited from BasePlot.
        self.compute_node_positions()
        # self.ax.set_xlim(-plot_radius*1.2, plot_radius*1.2)
        # self.ax.set_ylim(-plot_radius*1.2, plot_radius*1.2)
        # self.ax.xaxis.set_visible(False)
        # self.ax.yaxis.set_visible(False)
        # self.ax.set_aspect('equal')

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
            radius = circos_radius(n_nodes=len(self.graph.nodes()), node_r=1)
            x, y = get_cartesian(r=radius, theta=theta)
            xs.append(x)
            ys.append(y)
        self.node_coords = {'x': xs, 'y': ys}

    def draw_nodes(self):
        """
        Renders nodes to the figure.
        """
        node_r = self.nodeprops['r']
        for i, node in enumerate(self.nodes):
            x = self.node_coords['x'][i]
            y = self.node_coords['y'][i]
            self.nodeprops['facecolor'] = self.nodecolors[i]
            node_patch = patches.Ellipse((x, y), node_r, node_r,
                                         lw=0)
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
        circle = plt.Circle(xy=(x, y), radius=self.nodeprops['r'],
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
