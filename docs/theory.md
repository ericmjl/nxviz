# How to think about network visualizations

When you're asked to plot a network,
is your first instinct to reach for the "force-directed layout"?
If you try searching for the term on the internet, at first glance it sounds like not a bad idea.
But once you try plotting anything with a significant number of nodes
(one rule of thumb being 30 nodes or more),
the visualization descends into a hairball mess.

Is there a way out of this mess?

One answer to the question is yes,
and `nxviz` is intended to be an implementation of network visualizations in Python
that guides us network scientists towards thinking clearly about network visualizations.

## Grammar of graph visualizations

When we have a grammar of graphics,
we gain a framework to think about data visualization (in general).
In some senses, a grammar of graph visualizations is a subset of
a grammar of graphics.
What are the components of this grammar,
or in other words, the rules by which we compose together a network visualization?
Let's try to make sense of it.

### Prioritize node placement

The first step out of hairball hell
is to think clearly about where we want to place the nodes.
Why?
This is because nodes usually correspond to entities
that sometimes can be grouped and sorted.
For example, if a graph is constructed between people,
then we may wish to group them by some categorical property
(e.g. their hometown or school),
and perhaps sort them by some quantitative or ordinal property
(e.g. their age or time of entry into a venue).
If exact spatial placement is not meaningful
but relative spatial placement is,
then we might choose to place the nodes along some line segment,
such as a line, or a circle.

### Map node metadata to aesthetic properties

The node placement step brings us a major step out of hairball hell!
Once we are done with node placement,
we can go on to style the nodes in a data-driven fashion.
If you read and re-read and study the [Points of View][pov] column in Nature Methods,
as well as most other data visualization guides,
you'll see some patterns what _aesthetic_ properties of symbols
are most easily connected to data.

[pov]: http://blogs.nature.com/methagora/2013/07/data-visualization-points-of-view.html

For quantitative data:

1. Length and width are the easiest to map;
2. Area is the next easiest scale on which to perceive scale;
3. Transparency comes next,
4. Colour is the last.

In visualizing qualitative data, however, colour is an excellent first choice to begin with,
provided you don't have too many categories to visualize (12 is a good upper limit).

In a graph visualization, the most obvious aesthetic properties that we can control are:

1. The size (area) of nodes,
2. Their colour,
3. And their transparency.

### Draw edges

Once the nodes are drawn in, we next concern ourselves with how to draw edges.
In most graph visualizations, edges are represented using using lines between the nodes.
As such, we don't have to worry about the _layout_ of edges;
we only have to concern ourselves with the data-driven aesthetic styling of the edges.
The same principles apply above.

How the lines are drawn may vary from plot type to plot type.
For example, in a Hive plot, we may want to use Bezier curves to draw the lines,
but in an Arc plot, we may want to use circular arcs instead.
Meanwhile, in a Matrix plot, we might choose to use another shape to draw the edge
rather than draw in a line.
Either way, once we know the placement of the nodes,
then we know how to draw in the _relation_ between the two.

### Add in annotations

Once the node layout, node styling, and edge styling are complete,
we can add in annotations.
For example, if there are groupings of nodes present,
we can annotate the groups on the appropriate location.
If there are colour mappings to quantitative values,
then we might want to annotate the color bar on top.

### Add in highlights

The final piece is to selectively add in highlights onto the plot.
For example, we might wish to highlight a particular edge,
or a particular group of edges.
Or we might be interested in a particular node,
and all of the edges that connect that node to other nodes.
We might be concerned with in-edges only,
or out-edges only,
if we are dealing with a directed graph.

## Composability

`nxviz` is designed with composability in mind.
A pre-requisite of composability
is that we are thinking clearly
about what are independently-varying things
that we can add up together.
Shape and colour, for example, don't interfere with one another,
and might be considered independent.
Annotations can technically exist independent of node and edge drawing
(though it might not be particularly meaningful);
there's no deep-seated technical reason why we _have_ to couple them together.
Size and shape, by contrast, may get conflated with one another;
for example, a square of side 4 units
is going to be perceptually smaller than a circle of radius 4 units.
The `nxviz` API is designed such that
we can bring layout, styling, annotations and highlights in a composable fashion.

## Panels

Once we know how to build a single graph visualization,
we can extend the visualization through the principle of small multiples
to highlight interesting patterns in the graph data
that might be obscured looking at it in its totality.

What are the ways in which we might want to slice our data?
Because we are building discrete subplots using data,
the data we are mapping to each subplot
ideally should be categorical in nature.
Here's a few examples where we might want to do this.

**(1) Hive plots**

Hive plots are designed to show two or three groups of nodes and their connections.
They aren't designed to do more than three groups because of geometric constraints.
That said, we can work around this constraint by extracting triplet subgroups of nodes,
thus building a **hive panel**.

**(2) Focusing on edge categories**

We might wish to highlight different categories of edges
if the edges have categorical metadata available.
In each category, we select only a particular subset of edges to plot,
while preserving the node set.
In this way, we can get an arbitrary graph visualization panel
by simply filtering different edges to visualize.

**(3) Focusing on node categories**

This works similarly to edge categories,
except now, we filter the graph for certain categories of nodes.
Here, because the node set changes, the edge set will also change.

### `nxviz` graph filtering API

To support building panels,
the `nxviz` graph filtering API (located in the `nxviz.filter` submodule)
provides a few basic ways of filtering a graph.

1. Filtering edges by a categorical attribute.
2. Filtering nodes by a categorical attribute.
3. Filtering edges (all, in-edges, or out-edges) attached to a particular category of nodes.

Because the graph filtering step is usually the piece
that is the most hasslesome to write,
these are provided in the library.
