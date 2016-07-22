from .base import BasePlot
from .geometry import node_theta, get_cartesian
from collections import defaultdict
from matplotlib.path import Path

import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt

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

    def draw_edge(self, n1, n2):
        """

        """
