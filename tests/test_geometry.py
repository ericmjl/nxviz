from nxviz.geometry import circos_radius
import numpy as np


def test_circos_radius():
    """
    Uses the other triangle geometry rule to check that the radius is correct.
    """

    n_nodes = 10
    node_r = 1

    A = 2 * np.pi / n_nodes

    circ_r = 2 * node_r / np.sqrt(2 * (1 - np.cos(A)))

    assert np.allclose(circ_r, circos_radius(n_nodes, node_r))
