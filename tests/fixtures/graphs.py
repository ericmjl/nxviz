"""Graph generator fixtures."""

from itertools import cycle
import numpy as np
import networkx as nx
import pytest


categories = [
    "sun",
    "moon",
    "stars",
    "cloud",
    "wheel",
    "box",
    "plant",
    "chair",
    "slippers",
    "tablet",
    "laptop",
    "dishwasher",
    "bicycle",
    "piano",
    "laptop",
]
categorical = cycle(categories[0:3])
ordinal = cycle([1, 2, 3, 4, 5])
continuous = cycle(np.linspace(0, 3, 20))
many_categorical = cycle(categories)


@pytest.fixture
def dummyG():
    """Return a dummy graph."""
    return make_dummyG()


def make_dummyG():
    """Make an erdos-renyi graph."""
    n = 71
    p = 0.1
    G = nx.erdos_renyi_graph(n=n, p=p)

    # Add node metadata
    for n in G.nodes():
        G.nodes[n]["group"] = next(categorical)
        G.nodes[n]["value"] = next(ordinal)

    for u, v in G.edges():
        G.edges[u, v]["edge_value"] = next(continuous)

    return G


@pytest.fixture
def geoG():
    """Generate a geographic graph."""
    G = make_dummyG()
    for n in G.nodes():
        G.nodes[n]["longitude"] = np.random.normal()
        G.nodes[n]["latitude"] = np.random.normal()
    return G


@pytest.fixture
def manygroupG():
    """Generate graph with many categorical groups."""
    G = make_dummyG()
    for n in G.nodes():
        G.nodes[n]["group"] = next(many_categorical)

    return G


@pytest.fixture
def smallG():
    """Generate a small graph with 10 nodes."""
    G = nx.erdos_renyi_graph(n=10, p=0.15)
    return G
