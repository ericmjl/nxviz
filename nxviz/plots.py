"""Functions for plotting."""

import matplotlib.pyplot as plt
import networkx as nx


def despine(ax=None):
    """Remove all spines (and ticks) from the matplotlib axes."""
    if ax is None:
        ax = plt.gca()
    for spine in ax.spines:
        ax.spines[spine].set_visible(False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)


def respine(ax=None):
    """Reinstate the visibility of the spines.

    Use this when you want to make
    extremely fine-grained customizations to the plot axes
    and need to know where exactly to put markers.
    """
    if ax is None:
        ax = plt.gca()
    for spine in ax.spines:
        ax.spines[spine].set_visible(True)
    ax.xaxis.set_visible(True)
    ax.yaxis.set_visible(True)


def aspect_equal(ax=None):
    """Set aspect ratio of an axes object to be equal."""
    if ax is None:
        ax = plt.gca()
    ax.set_aspect("equal")


# The rescaling functions rescale the matplotlib axes.
# They all accept a graph, so that data-dependent xlim and ylims


def rescale(G: nx.Graph):
    """Default rescale."""
    ax = plt.gca()
    ax.relim()
    ax.autoscale_view()


def rescale_arc(G: nx.Graph):
    """Axes rescale function for arc plot."""
    ax = plt.gca()
    ax.relim()
    ymin, ymax = ax.get_ylim()
    maxheight = int(len(G)) + 1
    ax.set_ylim(ymin - 1, maxheight)
    ax.set_xlim(-1, len(G) * 2 + 1)


def rescale_square(G):
    """Axes rescale function to go square."""
    rescale(G)
    ax = plt.gca()
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    newmax = max([xmax, ymax, -xmin, -ymin])
    ax.set_xlim(-newmax, newmax)
    ax.set_ylim(-newmax, newmax)
