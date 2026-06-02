# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.8",
#     "matplotlib>=3.3.3",
#     "networkx>=2.5",
#     "numpy>=1.19.4",
#     "nxviz",
# ]
# [tool.uv.sources]
# nxviz = { path = "../..", editable = true }
# ///
import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mid-Level API

    As a graph visualization package built on top of NetworkX,
    `nxviz`'s design is highly inspired by the grammar of graphics.
    In particular, we see network visualizations
    as being composed of two main components,
    which correspond to the two objects that comprise a graph:

    1. Nodes: their layout (position, grouping & ordering), and visual styling (color, size, and transparency).
    2. Edges: their visual styling (color, width, and transparency).

    In addition to these,
    we may choose to add annotations and highlights
    onto the network visualization,
    such as node and/or edge labels,
    particular nodes and/or edges being highlighted,
    color bars or legends, and more.

    As such, the low-level functional API is designed around these ideas.
    In this notebook, we would like to highlight
    how the low-level API can be used
    to compose beautiful network visualizations,
    as long as one structures one's thinking around these principles.
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %load_ext autoreload
    # '%autoreload 2' command supported automatically in marimo
    # magic command not supported in marimo; please file an issue to add support
    # %config InlineBackend.figure_format = 'retina'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## An example graph

    To illustrate, we will use the Karate Club Graph from NetworkX's library.
    """)
    return


@app.cell
def _():
    import networkx as nx

    return (nx,)


@app.cell
def _(nx):
    from pathlib import Path

    data_dir = Path("docs/data")
    txt = (data_dir / "football.txt").read_text()
    gml = (data_dir / "football.gml").read_text()
    gml = gml.split("\n")[1:]
    G = nx.parse_gml(gml)
    print(txt)

    mapping = dict(
        {
            0: "Atlantic Coast",
            1: "Big East",
            2: "Big Ten",
            3: "Big Twelve",
            4: "Conference USA",
            5: "Independents",
            6: "Mid-American",
            7: "Mountain West",
            8: "Pacific Ten",
            9: "Southeastern",
            10: "Sun Belt",
            11: "Western Athletic",
        }
    )
    for node, data in G.nodes(data=True):
        G.nodes[node]["conference"] = mapping[data["value"]]
    return (G,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Visualization using NetworkX's built-in facilities

    NetworkX does come with its own built-in visualization facilities.
    Let's see what visualizations we get.
    """)
    return


@app.cell
def _(G, nx):
    nx.draw(G)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That looks a bit like a hairball. How can we make it look nicer?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Node Layout

    The first thing we should worry about is the node layout.
    This specifically refers to how nodes are positioned on the 2D plane.
    In a rational graph visualization,
    node placement should always take priority,
    as nodes represent entities with properties that we can grasp.

    The Circos plot layout lays out the nodes around the circumference of a circle.
    Hence, by stating up-front that we want a Circos layout,
    we take care of the first step of graph visualization,
    that is node placement.

    The `nodes` module provides a bunch of node drawing algorithms.
    They all take in the graph object `G` and return a position dictionary.
    That position dictionary is necessary for drawing edges, as we'll see in a moment.
    """)
    return


@app.cell
def _(G):
    from nxviz import nodes
    _pos = nodes.circos(G)
    return (nodes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Right now, it doesn't look like much - a blue donut, basically.
    That is because there are a bunch of circles of radius 1 (the default radius)
    that are overlapping with one another.
    To make things a bit more informative,
    we should probably group the nodes by their conference.

    Here is where nxviz's API becomes apparent.
    We can _refine_ the positioning of the nodes
    by specifying how to group them and sort them.
    This is accomplished by specifying
    the `group_by` and `sort_by` keyword arguments.
    Let's see the effect of specifying `group_by`:
    """)
    return


@app.cell
def _(G, nodes):
    _pos = nodes.circos(G, group_by='conference')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You might be wondering, why didn't that do anything?
    Actually, it did, but things are not yet visually apparent
    because we have only concerned ourselves with the _positions_ of the nodes
    and not the _visual properties_ of the nodes.
    The _visual properties_ of the node that can be mapped to data are
    the color, the transparency, and the node size.
    By default, node colors are blue,
    transparency (the alpha parameter in matplotlib) is 1,
    and node size is 1.
    Let's see how we can declare that we want our nodes to be coloured by conference
    while also being ordered by conference.
    """)
    return


@app.cell
def _(G, nodes):
    _pos = nodes.circos(G, group_by='conference', color_by='conference')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Things are starting to look promising!
    Though, if I were to comment on it, the plot is also still quite ugly.
    Let's start by applying a uniform scaling factor to all of the nodes
    to scale them to the size of the plot.
    (This is the `size_scale` encoding keyword argument that we'll be specifying below.)
    """)
    return


@app.cell
def _(G, nodes):
    _pos = nodes.circos(G, group_by='conference', color_by='conference')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The nodes look a bit more appropriately sized!
    The Circos plot still looks a bit squishy though.
    There's some _adjustments_ we need to do to the plot to make it look nice.
    We need to remove the spines and ticks to get rid of the boxiness effect.
    We also need to make the aspect ratio on the x- and y-axes equal.

    `despine()` will accomplish the first.
    """)
    return


@app.cell
def _(G, nodes):
    from nxviz.plots import aspect_equal, despine
    _pos = nodes.circos(G, group_by='conference', color_by='conference')
    despine()
    return aspect_equal, despine


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Putting it together with `aspect_equal()` will get us to a good starting point.
    """)
    return


@app.cell
def _(G, aspect_equal, despine, nodes):
    _pos = nodes.circos(G, group_by='conference', color_by='conference')
    despine()
    aspect_equal()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _Voila!_
    With the nodes rationally laid out,
    we have an awesome starting point for adding in the edges.

    Edge drawing requires that we have the positions of the nodes available.
    That we obtain from the `nodes.circos` (or other node drawing) function.
    We can then pass it to any of the edge drawing functions.

    When drawing edges, because we are drawing relations and not entities,
    we are no longer concerned with grouping and sorting.
    Instead, we are concerned with only the visual properties of the lines.
    The ones that are most easily mappable to data are:

    1. Line width
    2. Transparency
    3. Line color

    The `edges.circos` function is the most logical here, so we'll kick off with that one.
    """)
    return


@app.cell
def _(G, aspect_equal, despine, nodes):
    from nxviz import edges
    _pos = nodes.circos(G, group_by='conference', color_by='conference')
    edges.circos(G, _pos)
    despine()
    aspect_equal()
    return (edges,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    An alternative to drawing circos edges is to draw lines directly for each edge.
    """)
    return


@app.cell
def _(G, aspect_equal, despine, edges, nodes):
    _pos = nodes.circos(G, group_by='conference', color_by='conference')
    edges.line(G, _pos)
    despine()
    aspect_equal()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Regardless of which edge drawing method we choose,
    the chart might not be sufficiently ready for our purposes, though.
    After all, we have no idea what groups map to which color.
    If we _annotate_ the _circos group_ onto the plot,
    it becomes much clearer which colors map to which group.
    """)
    return


@app.cell
def _(G, aspect_equal, despine, edges, nodes):
    from nxviz import annotate
    _pos = nodes.circos(G, group_by='conference', color_by='conference')
    edges.circos(G, _pos)
    annotate.circos_group(G, group_by='conference')
    despine()
    aspect_equal()
    return (annotate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now it is clear that there are quite a lot of within-conference edges,
    and only some cross-conference edges between teams.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Other layouts
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Arc layout
    """)
    return


@app.cell
def _(G, annotate, aspect_equal, despine, edges, nodes):
    _pos = nodes.arc(G, group_by='conference', color_by='conference')
    edges.arc(G, _pos)
    annotate.arc_group(G, group_by='conference')
    despine()
    aspect_equal()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Parallel coordinates layout
    """)
    return


@app.cell
def _(G, annotate, aspect_equal, despine, edges, nodes):
    _pos = nodes.parallel(G, group_by='conference', color_by='conference')
    edges.line(G, _pos)
    annotate.parallel_group(G, group_by='conference')
    despine()
    aspect_equal()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The parallel coordinates layout might not necessarily be the most informative for this graph dataset,
    but we still show it here just to give you a flavour for what is possible with it.
    It may be more suited to bipartite graphs,
    which explicitly do not allow for edges within a single group.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Hive plot layout

    The hive plot is a bit special, in that it is suitable for only plotting a maximum of 3 groups.
    If we isolate nodes from just the Atlantic Coast, Independents, and Sun Belt,
    then we have a suitable way of plotting hive plots.

    Grouping is crucial to the Hive plot; we........

    Notice here that we take advantage of the `node_table` version of a graph's nodes,
    which is essentially a listing of all of the nodes and their properties.
    The node table works well for unipartite graphs,
    but needs to be modified for bipartite graphs.
    """)
    return


@app.cell
def _(G, annotate, aspect_equal, despine, edges, nodes):
    import numpy as np
    from nxviz.utils import node_table
    conferences = ['Atlantic Coast', 'Independents', 'Sun Belt']
    nt = node_table(G)
    wanted_nodes = nt.query('`conference` in @conferences').index
    G_sub = G.subgraph(wanted_nodes)
    size_scale = 0.5
    _pos = nodes.hive(G_sub, group_by='conference', color_by='conference')
    pos_cloned = nodes.hive(G_sub, group_by='conference', color_by='conference', layout_kwargs=dict(rotation=np.pi / 6))
    edges.hive(G_sub, _pos, pos_cloned=pos_cloned)
    annotate.node_colormapping(G_sub, color_by='conference')
    despine()
    aspect_equal()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here, we see an interesting pattern show up that might not have been visible earlier on:
    The Atlantic Coast teams have a lot of in-group edges than between-group edges,
    while the independents appear to have lots more between-group edges than in-group edges.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    This notebook's intent is to show you how the mid-level API of `nxviz`
    expresses a thought framework for drawing networks in a rational fashion.
    We start with a particular layout (positions) for the nodes,
    deciding on their grouping and ordering.
    We then declare their size, color, and transparency,
    based on data attributes that are present on there.

    Next, we declare the way to draw edges.
    Each layout has its own particular idiomatic edge drawing method,
    and usually the easiest way to handle this is to use the corresponding edges function.

    APIs that live at a higher level of abstraction usually imply more restrictions,
    as the intent here is usually to trade off customizable details for simplicity.
    The mid-level API allows us to gain finer-grained control over plots while remaining declarative.
    Changing the colormap, in particular, is out of scope for the mid-level API.

    The highest level of the `nxviz` API is object-based
    and opinionatedly pairs certain node layouts with certain edge drawing functions,
    not allowing for any customization there.
    The lowest-level API is where one interacts with the lines, layouts, positions directly,
    exposing more direct interaction with `matplotlib`.
    """)
    return


if __name__ == "__main__":
    app.run()
