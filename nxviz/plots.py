from .geometry import node_theta, get_cartesian, circos_radius
from .utils import (infer_data_type, num_discrete_groups, cmaps,
                    is_data_diverging)
from matplotlib.path import Path
from matplotlib.cm import get_cmap

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import networkx as nx


def despine(ax):
    for spine in ax.spines:
        ax.spines[spine].set_visible(False)
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)


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
                 edge_color=None, data_types=None, nodeprops=None,
                 edgeprops=None):
        super(BasePlot, self).__init__()
        # Set graph object
        self.graph = graph
        self.nodes = graph.nodes()  # keep track of nodes separately.

        # Set node arrangement
        self.node_order = node_order
        self.node_grouping = node_grouping
        self.group_and_sort_nodes()

        # Set node radius
        self.node_size = node_size

        # Set node colors
        self.node_color = node_color
        if self.node_color:
            self.node_colors = []
            self.compute_node_colors()
        else:
            self.node_colors = ['blue'] * len(self.nodes)

        # Set edge properties
        self.edge_width = edge_width
        self.edge_color = edge_color

        # Set data_types dictionary
        if not data_types:
            self.data_types = dict()
        else:
            self.check_data_types(data_types)
            self.data_types = data_types

        self.figure = plt.figure(figsize=(6, 6))
        self.ax = self.figure.add_subplot(1, 1, 1)
        despine(self.ax)

        # We provide the following attributes that can be set by the end-user.
        # nodeprops are matplotlib patches properties.
        if nodeprops:
            self.nodeprops = nodeprops
        else:
            self.nodeprops = {'radius': 1}
        # edgeprops are matplotlib line properties. These can be set after
        # instantiation but before calling the draw() function.
        if edgeprops:
            self.edgeprops = edgeprops
        else:
            self.edgeprops = {'facecolor': 'none',
                              'alpha': 0.2}

        # Compute each node's positions.
        self.compute_node_positions()

    def check_data_types(self, data_types):
        """
        Checks the data_types passed into the Plot constructor and makes sure
        that:
        - the values passed in belong to 'ordinal', 'categorical', or
          'continuous'.
        """
        for k, v in data_types.items():
            assert v in ['ordinal', 'categorical', 'continuous']

    def draw(self):
        self.draw_nodes()
        self.draw_edges()
        self.ax.relim()
        self.ax.autoscale_view()

    def compute_node_colors(self):
        """
        Computes the node colors.
        """
        data = [self.graph.node[n][self.node_color] for n in self.nodes]
        data_reduced = sorted(list(set(data)))
        dtype = infer_data_type(data)
        n_grps = num_discrete_groups(data)

        if dtype == 'categorical' or dtype == 'ordinal':
            cmap = get_cmap(cmaps['Accent_{0}'.format(n_grps)].mpl_colormap)
        elif dtype == 'continuous' and not is_data_diverging(data):
            cmap = get_cmap(cmaps['continuous'].mpl_colormap)
        elif dtype == 'continuous' and is_data_diverging(data):
            cmap = get_cmap(cmaps['diverging'].mpl_colormap)

        for d in data:
            idx = data_reduced.index(d) / n_grps
            self.node_colors.append(cmap(idx))

    def compute_node_positions(self):
        """
        Computes the positions of each node on the plot.

        Needs to be implemented for each plot type.
        """
        pass

    def draw_nodes(self):
        """
        Renders the nodes to the plot or screen.

        Needs to be implemented for each plot type.
        """
        pass

    def draw_edges(self):
        """
        Renders the nodes to the plot or screen.

        Needs to be implemented for each plot type.
        """
        pass

    def group_and_sort_nodes(self):
        """
        Groups and then sorts the nodes according to the criteria passed into
        the Plot constructor.
        """
        if self.node_grouping and not self.node_order:
            self.nodes = [n for n, d in
                          sorted(self.graph.nodes(data=True),
                                 key=lambda x: x[1][self.node_grouping])]

        elif self.node_order and not self.node_grouping:
            self.nodes = [n for n, _ in
                          sorted(self.graph.nodes(data=True),
                                 key=lambda x: x[1][self.node_order])]

        elif self.node_grouping and self.node_order:
            self.nodes = [n for n, d in
                          sorted(self.graph.nodes(data=True),
                                 key=lambda x: (x[1][self.node_grouping],
                                                x[1][self.node_order]))]


class CircosPlot(BasePlot):
    """
    Plotting object for CircosPlot.
    """
    def __init__(self, graph, node_order=None, node_size=None,
                 node_grouping=None, node_color=None, edge_width=None,
                 edge_color=None, data_types=None, nodeprops=None,
                 edgeprops=None):

        # Initialize using BasePlot
        BasePlot.__init__(self, graph, node_order=node_order,
                          node_size=node_size, node_grouping=node_grouping,
                          node_color=node_color, edge_width=edge_width,
                          edge_color=edge_color, data_types=data_types,
                          nodeprops=nodeprops, edgeprops=edgeprops)

    def compute_node_positions(self):
        """
        Uses the get_cartesian function to compute the positions of each node
        in the Circos plot.
        """
        xs = []
        ys = []
        node_r = self.nodeprops['radius']
        radius = circos_radius(n_nodes=len(self.graph.nodes()), node_r=node_r)
        self.plot_radius = radius
        self.nodeprops['linewidth'] = radius * 0.01
        for node in self.nodes:
            x, y = get_cartesian(r=radius, theta=node_theta(self.nodes, node))
            xs.append(x)
            ys.append(y)
        self.node_coords = {'x': xs, 'y': ys}

    def draw_nodes(self):
        """
        Renders nodes to the figure.
        """
        node_r = self.nodeprops['radius']
        lw = self.nodeprops['linewidth']
        for i, node in enumerate(self.nodes):
            x = self.node_coords['x'][i]
            y = self.node_coords['y'][i]
            color = self.node_colors[i]
            node_patch = patches.Circle((x, y), node_r,
                                        lw=lw, color=color,
                                        zorder=2)
            self.ax.add_patch(node_patch)

    def draw_edges(self):
        """
        Renders edges to the figure.
        """
        for i, (start, end) in enumerate(self.graph.edges()):
            start_theta = node_theta(self.nodes, start)
            end_theta = node_theta(self.nodes, end)
            verts = [get_cartesian(self.plot_radius, start_theta),
                     (0, 0),
                     get_cartesian(self.plot_radius, end_theta)]
            codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]

            path = Path(verts, codes)
            patch = patches.PathPatch(path, lw=1, **self.edgeprops, zorder=1)
            self.ax.add_patch(patch)


# class HivePlot(BasePlot):
#     """
#     Plotting object for HivePlot.
#     """
#     def __init__(self, graph, node_order=None, node_size=None,
#                  node_grouping=None, node_color=None, edge_width=None,
#                  edge_color=None, data_types=None):
#
#         # Initialize using BasePlot
#         BasePlot.__init__(self, graph, node_order=node_order,
#                           node_size=node_size, node_grouping=node_grouping,
#                           node_color=node_color, edge_width=edge_width,
#                           edge_color=edge_color, data_types=data_types)
#
#     def set_xylims(self):
#         pass
#
#     def set_nodes(self, nodes):
#         """
#         Sets the nodes attribute.
#
#         Checks that `nodes` is a dictionary where the key is the group ID and
#         the value is a list of nodes that belong in that group.
#         """
#         assert isinstance(nodes, dict), 'nodes must be a dictionary'
#         for k, v in nodes.items():
#             assert isinstance(v, list) or isinstance(v, tuple),\
#                 'each value in the dictionary must be a list or tuple'
#         assert len(nodes.keys()) in [2, 3], 'there can only be 2 or 3 groups'
#
#         self.nodes = nodes
#
#     def set_major_angle(self):
#         """
#         Sets the major angle between the plot groups, in radians.
#         """
#         self.major_angle = 2 * np.pi / len(self.nodes.keys())
#
#     def set_minor_angle(self):
#         """
#         Sets the minor angle between the plot groups, in radians.
#         """
#         self.minor_angle = 2 * np.pi / 12
#
#     def set_nodecolors(self, nodecolors):
#         """
#         Sets the nodecolors.
#
#         `nodecolors` can be specified as either a single string, or as a
#         dictionary of group_identifier:strings.
#
#         Performs type checking to ensure that nodecolors is specified as a
#         dictionary where the keys must match up with the .nodes attribute.
#
#         Otherwise
#         """
#         assert isinstance(nodecolors, dict) or isinstance(nodecolors, str)
#         if isinstance(nodecolors, dict):
#             assert set(nodecolors.keys()) == set(self.nodes.keys())
#             self.nodecolors = nodecolors
#         elif isinstance(nodecolors, str):
#             self.nodecolors = dict()
#             for k in self.nodes.keys():
#                 self.nodecolors[k] = nodecolors
#
#     def has_edge_within_group(self, group):
#         """
#         Checks whether there are within-group edges or not.
#         """
#         assert group in self.nodes.keys(),\
#             "{0} not one of the group of nodes".format(group)
#         nodelist = self.nodes[group]
#         for n1, n2 in self.edges:
#             if n1 in nodelist and n2 in nodelist:
#                 return True
#
#     def compute_node_positions(self):
#         """
#         Computes the positions of each node on the plot.
#
#         Sets the node_coords attribute inherited from BasePlot.
#         """
#         xs = defaultdict(lambda: defaultdict(list))
#         ys = defaultdict(lambda: defaultdict(list))
#         for g, (grp, nodes) in enumerate(self.nodes.items()):
#             if self.has_edge_within_group(grp):
#                 for r, node in enumerate(nodes):
#                     theta = g * self.major_angle - self.minor_angle
#                     x, y = get_cartesian(r+2, theta)
#                     xs[grp]['minus'].append(x)
#                     ys[grp]['minus'].append(y)
#
#                     theta = g * self.major_angle + self.minor_angle
#                     x, y = get_cartesian(r+2, theta)
#                     xs[grp]['plus'].append(x)
#                     ys[grp]['plus'].append(y)
#             else:
#                 for r, node in enumerate(nodes):
#                     theta = g * self.major_angle
#                     x, y = get_cartesian(r+2, theta)
#                     xs[grp]['axis'].append(x)
#                     ys[grp]['axis'].append(y)
#         self.node_coords = dict(x=xs, y=ys)
#
#     def draw_nodes(self):
#         """
#         Renders nodes to the figure.
#         """
#         for grp, nodes in self.nodes.items():
#             for r, n in enumerate(nodes):
#                 if self.has_edge_within_group(grp):
#                     x = self.node_coords['x'][grp]['minus'][r]
#                     y = self.node_coords['y'][grp]['minus'][r]
#                     self.draw_node(grp, x, y)
#
#                     x = self.node_coords['x'][grp]['plus'][r]
#                     y = self.node_coords['y'][grp]['plus'][r]
#                     self.draw_node(grp, x, y)
#
#                 else:
#                     x = self.node_coords['x'][grp]['axis'][r]
#                     y = self.node_coords['y'][grp]['axis'][r]
#                     self.draw_node(grp, x, y)
#
#     def draw_node(self, group, x, y):
#         """
#         Convenience function for simplifying the code in draw_nodes().
#         """
#         circle = plt.Circle(xy=(x, y), radius=self.nodeprops['r'],
#                             color=self.nodecolors[group], linewidth=0)
#         self.ax.add_patch(circle)
#
#     def draw_edges(self):
#         """
#         Renders the edges to the figure.
#         """
#         pass
#
#     def draw_edge(self, n1, n2):
#         """
#
#         """
#         pass


class MatrixPlot(BasePlot):
    """
    Plotting object for the MatrixPlot.
    """
    def __init__(self, graph, node_order=None, node_size=None,
                 node_grouping=None, node_color=None, edge_width=None,
                 edge_color=None, data_types=None, nodeprops=None,
                 edgeprops=None):

        # Initialize using BasePlot
        BasePlot.__init__(self, graph, node_order=node_order,
                          node_size=node_size, node_grouping=node_grouping,
                          node_color=node_color, edge_width=edge_width,
                          edge_color=edge_color, data_types=data_types,
                          nodeprops=nodeprops, edgeprops=edgeprops)

        # The following atribute is specific to MatrixPlots
        self.cmap = cmaps['continuous'].mpl_colormap

    def draw(self):
        """
        Draws the plot to screen.
        """
        matrix = nx.to_numpy_matrix(self.graph, nodelist=self.nodes)
        self.ax.matshow(matrix, cmap=self.cmap)


class ArcPlot(BasePlot):
    """
    Plotting object for ArcPlot.
    """
    def __init__(self, graph, node_order=None, node_size=None,
                 node_grouping=None, node_color=None, edge_width=None,
                 edge_color=None, data_types=None, nodeprops=None,
                 edgeprops=None):

        # Initialize using BasePlot
        BasePlot.__init__(self, graph, node_order=node_order,
                          node_size=node_size, node_grouping=node_grouping,
                          node_color=node_color, edge_width=edge_width,
                          edge_color=edge_color, data_types=data_types,
                          nodeprops=nodeprops, edgeprops=edgeprops)

    def compute_node_positions(self):
        """
        Computes nodes positions.

        Arranges nodes in a line starting at (x,y) = (0,0). Node radius is
        assumed to be equal to 0.5 units. Nodes are placed at integer
        locations.
        """
        xs = []
        ys = []

        for node in self.nodes:
            xs.append(self.nodes.index(node))
            ys.append(0)

        self.node_coords = {'x': xs, 'y': ys}

    def draw_nodes(self):
        """
        Draw nodes to screen.
        """
        node_r = 1
        for i, node in enumerate(self.nodes):
            x = self.node_coords['x'][i]
            y = self.node_coords['y'][i]
            color = self.node_colors[i]
            node_patch = patches.Ellipse((x, y), node_r, node_r,
                                         lw=0, color=color, zorder=2)
            self.ax.add_patch(node_patch)

    def draw_edges(self):
        """
        Renders edges to the figure.
        """
        for i, (start, end) in enumerate(self.graph.edges()):
            start_idx = self.nodes.index(start)
            start_x = self.node_coords['x'][start_idx]
            start_y = self.node_coords['y'][start_idx]

            end_idx = self.nodes.index(end)
            end_x = self.node_coords['x'][end_idx]
            end_y = self.node_coords['y'][end_idx]

            arc_radius = abs(end_x - start_x) / 2
            # we do min(start_x, end_x) just in case start_x is greater than
            # end_x.
            middle_x = min(start_x, end_x) + arc_radius
            middle_y = arc_radius * 2

            verts = [(start_x, start_y),
                     (middle_x, middle_y),
                     (end_x, end_y)]

            codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]

            path = Path(verts, codes)
            patch = patches.PathPatch(path, lw=1, **self.edgeprops, zorder=1)
            self.ax.add_patch(patch)

    def draw(self):
        self.draw_nodes()
        self.draw_edges()
        xlimits = (-1, len(self.nodes) + 1)
        # halfwidth = len(self.nodes) + 1 / 2
        # ylimits = (-halfwidth, halfwidth)
        self.ax.set_xlim(*xlimits)
        self.ax.set_ylim(*xlimits)
