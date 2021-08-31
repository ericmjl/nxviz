# Library Architecture

`nxviz`'s architecture, or how the code is organized,
follows the logical structure of prioritizing nodes' positioning over edges.
As such, there are multiple API layers.
We have documentation on how to use each of those API layers,
so we won't go through them too closely here.

## High level

At the high level, we provide the following plots in the `nxviz` main namespace:

- Graph visualizations with no cloned axes
    - `arc`: Arc plots
    - `circos`: Circos plots
    - `parallel`: Parallel coordinate plots
- Graph visualizations with cloned axes
    - `hive`: Hive plots
    - `matrix`: Matrix plots

The intent for this level of API is to provide
a single function call that enables users to draw a graph to screen.

### Intended usage example

```python
import nxviz as nv
ax = nv.hive(G, group_by="group", sort_by="value", node_color_by="value")
```

## Medium Level

At the medium level API,
users interact with node layout and plotting functions in `nxviz.nodes`
as well as edge drawing functions in `nxviz.edges`.
Mostly it provides a way to compose
node rendering and edge rendering.

Mapping from quantitative or qualitative data
is still done by nxviz's built-in default functions,
and can't be changed at this level.

### Intended usage example

Here is an example of how one would use the mid-level API.

```python
from nxviz import nodes, edges

pos = nodes.circos(G, group_by="group", sort_by="value", color_by="group")
edges.circos(G, pos, alpha_by="edge_value")
```

## Low Level

At the low level API, `nxviz` provides users with
the maximum amount of control over node and edge styling.
Here, instead of passing graph objects into the plotting and layout functions,
users interact with node and edge tables.

For node plotting, the steps are:

1. Obtain the node table
2. Using the node table, obtain the node positions using a node layout function.
2. Using the node table, obtain node color, transparency, and sizes based on node metadata.
3. Finally, obtain the matplotlib patches, and add them to the plot.

For edge plotting, the steps are:

1. Obtain the edge table
2. Using the edge table, obtain the edge color, transparency and line widths based on edge metadata.
3. Finally, obtain the matplotlib patches, and add them to the plot.

### Intended usage example

Here's an example of how one would use the low-level API.


```python
from nxviz import lines

ax = plt.gca()

##### Part 1: Nodes #####
# 1. Obtain node table
nt = utils.node_table(G)

# 2. Obtain positions using node table.
pos = layouts.circos(nt, group_by="group", sort_by="value")

# 3. Obtain node styles
node_color = group_colormap(nt["group"])
alpha = nodes.transparency(nt, alpha_by=None)
size = nodes.node_size(nt, "value")

# 4. Obtain patches styled correctly and add them to matplotlib axes.
patches = nodes.node_glyphs(
    nt, pos, node_color=node_color, alpha=alpha, size=size
)
for patch in patches:
    ax.add_patch(patch)

##### Part 2: Edges #####
# 1. Obtain edge table
et = utils.edge_table(G)

# 2. Obtain edge styling.
edge_color = edges.edge_colors(et, nt=None, color_by=None, node_color_by=None)
lw = np.sqrt(et["edge_value"])
alpha = edges.transparency(et, alpha_by=None)

# 3. Obtain edge patches styled and add them to matplotlib axes.
patches = lines.circos(
    et, pos, edge_color=edge_color, alpha=alpha, lw=lw, aes_kw={"fc": "none"}
)
for patch in patches:
    ax.add_patch(patch)
```

## Plotting utilities

We include some plotting utilities
to make composing new plots together a bit easier.
These functions are located in the `nxviz.plots` module.
These include functions to rescale matplotlib axes (`plots.rescale()`),
and despine and re-spine the axes objects
(`plots.despine()` and `plots.respine()`).

## Annotations

The core node and edge drawing functions
can be composed with a variety of annotations onto the axes.
These are all located in the `nxviz.annotate` module.
For example, if one wants to add grouping annotations onto a Circos plot,
one would use `annotate.circos_group`.
Or if one wants to add in group block diagonals to the Matrix plot,
one would call `annotate.matrix_block`.

## Visual Encodings

The default functions for mapping data to
visual properties of node and edges
are located in the `nxviz.nodes` and `nxviz.edges` modules.
Underneath the hood, however,
they call on functions in the `encodings` module.

The pattern here is to produce an iterable of colors
that correspond to each node and edge,
done in a data-driven fashion.
Underneath the hood, for code conciseness,
we take advantage of the pandas DataFrame and Series APIs.

## Geometry

The `nxviz.polcart` and `nxviz.geometry` modules
give us convenience functions
for calculating (x, y) coordinates from polcar coordinates
and doing trigonometric calculations.
(These are heavily used in plots with circular layouts,
such as the Circos and Hive plots.)

## Utils

The `nxviz.utils` module is a catch-all
for utility functions that don't fall into the aforementioned categories.
For example, the node and edge table functions
(`utils.node_table(G)` and `utils.edge_table(G)`),
which construct the pandas DataFrame versions of the node set and edge set,
are located in there.
Because grouping and sorting nodes are intrinsic
to constructing rational graph visualizations,
the function `utils.group_and_sort(nt)` is also provided in there.
Finally, there are utilities for automatically inferring
whether a column of data is categorical,
ordinal,
or continuous based on data types and ranges.
(That is used for identifying colormaps to be used for a particular data.)
