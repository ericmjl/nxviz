from .base import BasePlot
from .geometry import node_theta, get_cartesian, major_angle
from collections import defaultdict
from matplotlib.path import Path

import matplotlib.patches as patches
import numpy as np


class HivePlot(BasePlot):
    """
    Plotting object for HivePlot.
    """
    def __init__(self, nodes, edges, node_radius=0.5,
                 nodecolors='blue', edgecolors='black',
                 nodeprops=dict(), edgeprops=dict(),
                 figsize=(8, 8)):
        # Initialize the BasePlot
        BasePlot.__init__(self, nodes, edges)

        # The following method calls are specific to HivePlot.
        # 1. Set the .nodes attribute, but first do type checking.
        self.set_nodes(nodes)
        # 2. Set the major and minor angle attributes.
        self.set_major_angle()
        self.set_minor_angle()
        # 3. Set the nodecolors attributes.
        self.set_nodecolors(nodecolors)

        self.ax.set_aspect('equal')

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
        self.major_angle = 2 * np.pi / len(nodes.keys())

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
            assert set(nodecolors.keys()) == set(nodes.keys())
        self.nodecolors = nodecolors

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
                    theta = self.major_angle - angle
                    x, y = get_cartesian(r+2, theta)
                    xs[grp]['minus'].append(x)
                    ys[grp]['minus'].append(y)

                    theta = self.major_angle + angle
                    x, y = get_cartesian(r+2, theta)
                    xs[grp]['plus'].append(x)
                    ys[grp]['plus'].append(y)
            else:
                for r, node in enumerate(nodes):
                    theta = self.major_angle + angle
                    x, y = get_cartesian(r+2, theta)
                    xs[grp]['axis'].append(x)
                    ys[grp]['axis'].append(y)
        self.node_coords = dict('x': xs, 'y': ys)

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
        Convenience function for flattening the logic in draw_nodes().
        """
        circle = plt.Circle(xy=(x, y), radius=self.node_radius,
                            color=self.nodecolors[group], linewidth=0)

    def draw_edges(self):
        """
        Renders the edges to the figure.
        """
        
