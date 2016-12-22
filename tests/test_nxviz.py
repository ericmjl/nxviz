from hypothesis import given, assume
from hypothesis.strategies import lists, integers,
from nxviz.plots import BasePlot


@given(lists(integers(), unique=True),
       lists(integers(), unique=True, min_size=2, max_size=2))
def test_initialization(nodes, edges):
    assume(len(nodes) > 2 and len(nodes) < 5)
    assume(len(edges) > 1 and len(edges) < 5)
    b = BasePlot(nodes, edges)
    assert b.nodecolors == ['blue'] * len(b.nodes)
    assert b.edgecolors == ['black'] * len(b.edges)
