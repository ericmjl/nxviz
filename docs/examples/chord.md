---
title: Chord Diagram
marimo-version: 0.23.8
header: |-
  # /// script
  # requires-python = ">=3.12"
  # dependencies = [
  #     "marimo>=0.23.8",
  #     "matplotlib>=3.3.3",
  #     "networkx>=2.5",
  #     "nxviz",
  # ]
  # [tool.uv.sources]
  # nxviz = { path = "../..", editable = true }
  # ///
---

```python {.marimo}
import marimo as mo
```

# Chord Diagram

The chord diagram aggregates nodes into arc segments and edges into ribbons,
showing **aggregate flow between groups** rather than individual connections.

This is ideal for visualizing migration patterns, trade flows,
information exchange, or any network where you want to see
how much moves between categories rather than individual links.

In this notebook we use synthetic **population migration data** between continents.

```python {.marimo}
import networkx as nx

import nxviz as nv
```

## Build the Graph

Each node is a country with a `continent` attribute.
Each edge is a migration flow with a `flow` weight.

```python {.marimo}
G = nx.DiGraph()

continents = {
    "Nigeria": "Africa",
    "Egypt": "Africa",
    "South Africa": "Africa",
    "China": "Asia",
    "India": "Asia",
    "Japan": "Asia",
    "Germany": "Europe",
    "France": "Europe",
    "UK": "Europe",
    "USA": "N. America",
    "Canada": "N. America",
    "Mexico": "N. America",
    "Brazil": "S. America",
    "Argentina": "S. America",
    "Australia": "Oceania",
    "New Zealand": "Oceania",
}

for country, continent in continents.items():
    G.add_node(country, continent=continent)

flows = [
    ("India", "UK", 500000),
    ("India", "USA", 800000),
    ("Mexico", "USA", 1200000),
    ("China", "USA", 400000),
    ("Nigeria", "UK", 300000),
    ("France", "UK", 200000),
    ("Brazil", "USA", 300000),
    ("UK", "Australia", 250000),
    ("Germany", "USA", 200000),
    ("Egypt", "France", 150000),
    ("South Africa", "UK", 200000),
    ("China", "Australia", 350000),
    ("India", "Canada", 250000),
]

for src, tgt, flow in flows:
    G.add_edge(src, tgt, flow=flow)

print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
```

## Basic Chord Diagram

The `group_by` parameter is required — it tells nxviz which node attribute
defines the groups. The `weight_by` parameter specifies the edge attribute
to aggregate (ribbon width will be proportional to total flow).

```python {.marimo}
nv.chord(G, group_by="continent", weight_by="flow")
```

## Reading the Diagram

- **Arc segments** around the circle represent groups (continents).
  Arc width is proportional to the number of nodes in each group.
- **Ribbons** connect arc segments. Each ribbon shows aggregate flow
  from one group to another.
- **Ribbon color** matches the source group, so you can see directionality.
- **Ribbon width** at each end is proportional to the flow volume.

## Customizing Appearance

Use `alpha` to control ribbon transparency.

```python {.marimo}
nv.chord(
    G,
    group_by="continent",
    weight_by="flow",
    alpha=0.6,
)
```

## Unweighted Chord Diagram

If `weight_by` is omitted, each edge counts equally.
This is useful when you only care about the **number of connections**
between groups, not the volume.

```python {.marimo}
nv.chord(G, group_by="continent")
```

## Interactive Chord Diagram (Plotly Backend)

Switch to the plotly backend for hover tooltips, zoom, and pan.
Hover over a ribbon to see the source/target groups and flow weight.

```python {.marimo}
fig = nv.chord(
    G,
    group_by="continent",
    weight_by="flow",
    backend="plotly",
)
fig
```
