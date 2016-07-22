from .base import BasePlot
from .geometry import node_theta, get_cartesian
from matplotlib.path import Path

import matplotlib.patches as patches


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
