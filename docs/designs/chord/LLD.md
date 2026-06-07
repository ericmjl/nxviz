# Chord Diagram - Low-Level Design

**Created**: 2026-06-07
**HLD Link**: ../../high-level-design.md

## Overview

A chord diagram is a circos-plot variant that aggregates nodes into arc segments and edges into ribbons, showing aggregate flow between groups. Unlike the existing circos plot which draws individual nodes and edges, the chord diagram operates at the group level — making it ideal for visualizing inter-group relationships like migration patterns, trade flows, or information exchange.

This is a new plot type (`nv.chord`) that reuses the existing compute/render architecture but introduces a distinct pipeline: group arc layout, edge aggregation, and ribbon rendering.

## Context

nxviz currently supports six plot types (circos, arc, hive, matrix, parallel, geo), all of which operate on individual nodes and edges. The chord diagram is the first plot type that aggregates to the group level. It targets the same user base — researchers and analysts exploring network data — but serves a different need: summarizing patterns across categorical groupings rather than inspecting individual connections.

The canonical use case is population flow between continents: countries (nodes) grouped into continents, with migration flows (weighted edges) aggregated into ribbons showing how many people move between continent pairs.

## Architecture

```
User Call: nv.chord(G, group_by="continent", weight_by="flow")
    │
    ▼
┌─────────────────── COMPUTE PHASE (backend-agnostic) ───────────────────┐
│                                                                        │
│  utils.node_table(G)  →  chord.group_arcs(nt, group_by)               │
│                               →  group_arcs: DataFrame                 │
│                                  [group, start_angle, end_angle,       │
│                                   n_nodes, color]                      │
│                                                                        │
│  utils.edge_table(G)  →  chord.aggregate_edges(et, nt, group_by,      │
│                                                  weight_by)            │
│                               →  agg_edges: DataFrame                  │
│                                  [source_group, target_group, weight]  │
│                                                                        │
│  chord.ribbon_coords(agg_edges, group_arcs, radius)                    │
│                               →  ribbon_data: List[Dict]               │
│                                  each with path_coords, width, color   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────── RENDER PHASE (backend-specific) ───────────────────┐
│                                                                        │
│  backend.draw_arcs(axes, group_arcs, radius)                           │
│  backend.draw_ribbons(axes, ribbon_data)                               │
│  backend.draw_arc_labels(axes, group_arcs, radius)                     │
│  backend.despine(axes)                                                 │
│  backend.set_aspect_equal(axes)                                        │
│  backend.rescale(axes, pos_data, "default")                            │
│  return backend.get_figure(axes)                                       │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

## Data Models

### GroupArcs

Computed by `chord.group_arcs()` from the node table.

| Field | Type | Description |
|-------|------|-------------|
| group | Hashable | Group identifier (e.g., "Africa", "Asia") |
| start_angle | float | Starting angle in radians (inclusive) |
| end_angle | float | Ending angle in radians (exclusive) |
| n_nodes | int | Number of nodes in this group |
| color | tuple | RGBA color assigned to this group |

Angular gap: A small configurable gap (default `2π × 0.01` radians per group) separates adjacent arcs for visual clarity. Arcs are sized proportionally to `n_nodes` within the remaining angular space.

### AggEdges

Computed by `chord.aggregate_edges()` from the edge table and node table.

| Field | Type | Description |
|-------|------|-------------|
| source_group | Hashable | Group of the source node |
| target_group | Hashable | Group of the target node |
| weight | float | Sum of edge weights (or count of edges if unweighted) |

For undirected graphs, each edge contributes to both (A→B) and (B→A) rows (mirroring existing `edge_table` behavior). For directed graphs, source and target are preserved as-is. Self-loops (A→A) are included.

### RibbonData

Computed by `chord.ribbon_coords()` from group arcs and aggregated edges.

Each ribbon is a dictionary:

| Field | Type | Description |
|-------|------|-------------|
| source_group | Hashable | Source group |
| target_group | Hashable | Target group |
| source_angle_start | float | Start angle on source arc |
| source_angle_end | float | End angle on source arc |
| target_angle_start | float | Start angle on target arc |
| target_angle_end | float | End angle on target arc |
| path_coords | np.ndarray | Shape (N, 2) — Bezier path through center |
| color | tuple | RGBA color (of source group) |
| alpha | float | Transparency value |

Ribbon width at each arc is proportional to the flow weight relative to total flow on that arc. Each arc's angular extent is split into a source zone (outgoing) and a target zone (incoming), each proportional to total outgoing/incoming flow. Within each zone, individual ribbons get sub-bands proportional to their weight share. This two-phase allocation guarantees that source and target sub-bands on the same arc never overlap angularly.

### Directionality: target-gap offset

To make flow direction visually clear, the **target end** of each ribbon is offset inward from the arc by 3% of the radius. The source end remains attached to the arc at `inner_r`.

| End | Anchor radius | Visual effect |
|-----|--------------|---------------|
| Source (start) | `inner_r = radius × (1 - arc_width/2)` | Flush with the arc — no gap |
| Target (end) | `target_r = inner_r - 0.03 × radius` | 3% gap between ribbon edge and arc |

This creates a visible detachment at the target end, making it easy to distinguish "where flow comes from" (attached) from "where flow goes to" (detached). The gap is proportional to radius so it scales correctly at any size.

For self-loops (A→A), both source and target sub-bands lie on the same arc. The target-gap offset is especially important here: without it, the source and target bands overlap on the arc, making the self-loop appear to fill the entire arc segment.

## New Module: `nxviz/chord.py`

This module contains all compute-phase functions for the chord diagram. It is the chord-specific equivalent of what `layouts.py` + `paths.py` provide for other plot types.

### `group_arcs(nt, group_by, palette=None)`

Takes the node table and returns the GroupArcs DataFrame.

1. Count nodes per group.
2. Sort groups by a deterministic order (sorted alphabetically by default).
3. Compute total angular gap: `n_groups × gap_per_group`.
4. Available angular space: `2π - total_gap`.
5. Assign each group an angular extent proportional to its node count.
6. Assign colors using the existing `encodings.color_func()` pipeline applied to group labels.

### `aggregate_edges(et, nt, group_by, weight_by=None)`

Takes the edge table, node table, and returns the AggEdges DataFrame.

1. Build a `node → group` mapping from the node table.
2. Map each edge's source and target to their groups.
3. Group by `(source_group, target_group)`.
4. If `weight_by` is specified, sum the weight column. Otherwise, count rows.
5. Return aggregated DataFrame.

### `ribbon_coords(agg_edges, group_arcs, radius)`

Takes aggregated edges and group arcs, returns list of RibbonData dicts.

**Sub-band allocation** — each group's arc is divided into two contiguous zones: source sub-bands (for outgoing flows) followed by target sub-bands (for incoming flows). This two-phase allocation uses a single tracker per arc, guaranteeing zero angular overlap between source and target sub-bands on the same arc.

1. **Budget split**: For each group, the arc's total angular extent is divided proportionally between source and target zones based on total outgoing vs incoming flow. If group A sends 1.2M and receives 3.15M, the source zone gets `arc_extent × 1.2M / (1.2M + 3.15M)` and the target zone gets the remainder.
2. **Phase 1 — source sub-bands**: For each edge, allocate a source sub-band proportional to `weight / outgoing_flow` within the source zone. The tracker advances forward. Source sub-bands are ordered by target group index to minimise ribbon crossings.
3. **Phase 2 — target sub-bands**: Target trackers start where source trackers ended. For each edge, allocate a target sub-band proportional to `weight / incoming_flow` within the target zone.
4. Both phases fit within the arc boundary by construction.

For each aggregated edge (A→B):
1. Look up A's source sub-band angles and B's target sub-band angles.
2. Compute Cartesian coordinates at two anchor radii:
   - Source arc segment at `inner_r` (attached to the arc).
   - Target arc segment at `target_r = inner_r - 0.03 × radius` (detached for directionality).
3. Generate a Bezier path through the center connecting the two arc segments.
4. Build the RibbonData dict.

For self-loops (A→A), the source sub-band occupies the first portion of A's arc and the target sub-band follows immediately after. The `_self_loop_path` function draws a loop from the source sub-band through the interior back to the target sub-band, using a control radius of `inner_r × 0.5` so the loop stays well inside the circle. The target-gap offset (`target_r < inner_r`) provides visual separation at the arc boundary.

## Backend Protocol Extension

Two new methods on `PlotBackend`:

### `draw_arcs(axes, group_arcs, radius)`

Draws arc segments around the circle. Each arc is a thick colored band (arc path with linewidth proportional to a configurable band width, default 20px). In matplotlib, this is a `matplotlib.patches.Arc` or a series of line segments along the arc path with thick linewidth. In plotly, a `go.layout.Shape` with path type arc.

### `draw_ribbons(axes, ribbon_data)`

Draws ribbons connecting arc segments. Each ribbon is a filled polygon with transparency and a full-opacity border to visually separate overlapping ribbons and preserve the directionality cue (attached source end vs detached target end). In matplotlib, a `matplotlib.patches.Polygon` or `PathPatch`. In plotly, a filled `go.Scatter` or `go.Scatterpolar`. Interactive backends (plotly) support hover highlighting: the hovered ribbon transitions to full opacity while others dim, with borders following the same transition.

### `draw_arc_labels(axes, group_arcs, radius)`

Draws group labels outside each arc at the midpoint angle. In matplotlib, `axes.text()` with rotation. In plotly, text annotations.

Existing backend methods (`despine`, `set_aspect_equal`, `rescale`, `get_figure`) are reused as-is.

## API Integration

### `nxviz/api.py`

A new `chord` function, structured like existing plot types:

```python
chord = partial(
    base_chord,
    group_by=None,
)
update_wrapper(chord, base_chord)
chord.__name__ = "api.chord"
```

A new `base_chord` function replaces the node/edge pipeline with the chord-specific pipeline:

```python
def base_chord(
    G: nx.Graph,
    group_by: Hashable,
    weight_by: Hashable = None,
    sort_by: Hashable = None,
    node_palette=None,
    edge_palette=None,
    backend: str = "matplotlib",
):
```

Key differences from `base`:
- No individual node drawing — replaced by arc drawing.
- No individual edge drawing — replaced by ribbon drawing.
- `weight_by` replaces `edge_color_by`, `edge_lw_by`, etc. (ribbon width encodes weight).
- The `sort_by` parameter controls ordering of groups around the circle.

### `nxviz/__init__.py`

Export `chord` alongside existing plot functions.

## Edge Cases

1. **Single group**: One arc covers the full circle. All ribbons are self-loops. Render a warning since this is rarely useful.
2. **Two groups**: Two arcs with a gap. Ribbons connect the two arcs. Self-loops render as small loops on each arc.
3. **Empty group**: A group with zero nodes produces no arc. Raise ValueError — every group must have at least one node.
4. **No edges between groups**: Ribbons are absent. Arcs still render. Not an error.
5. **Self-loops only**: All flow stays within groups. Ribbons loop back on the same arc.
6. **Unequal group sizes**: Large groups get proportionally wider arcs. Very small groups (1-2 nodes) may produce thin arcs — the gap size bounds the minimum visual thickness.
7. **Very large number of groups**: Performance degrades with O(n_groups²) ribbons. Cap at a warning threshold (e.g., 20 groups).
8. **Zero-weight edges**: Edges with zero weight contribute nothing to the aggregation. They are silently dropped.

## Dependencies

No new external dependencies. The chord diagram uses:
- `numpy` — trigonometry for arc/ribbon coordinates
- `pandas` — groupby/aggregation
- Existing `nxviz.polcart`, `nxviz.geometry`, `nxviz.encodings`, `nxviz.utils` modules

## Reference Use Case: Population Flow Between Continents

The motivating example uses synthetic migration data:

```python
import networkx as nx
import nxviz as nv

G = nx.DiGraph()

continents = {
    "Nigeria": "Africa", "Egypt": "Africa", "South Africa": "Africa",
    "China": "Asia", "India": "Asia", "Japan": "Asia",
    "Germany": "Europe", "France": "Europe", "UK": "Europe",
    "USA": "N. America", "Canada": "N. America", "Mexico": "N. America",
    "Brazil": "S. America", "Argentina": "S. America",
    "Australia": "Oceania", "New Zealand": "Oceania",
}

for country, continent in continents.items():
    G.add_node(country, continent=continent)

flows = [
    ("India", "UK", 500000), ("India", "USA", 800000),
    ("Mexico", "USA", 1200000), ("China", "USA", 400000),
    ("Nigeria", "UK", 300000), ("France", "UK", 200000),
    ("Brazil", "USA", 300000), ("UK", "Australia", 250000),
    ("Germany", "USA", 200000), ("Egypt", "France", 150000),
    ("South Africa", "UK", 200000), ("China", "Australia", 350000),
    ("Argentina", "Spain", 300000), ("India", "Canada", 250000),
]

for src, tgt, flow in flows:
    G.add_edge(src, tgt, flow=flow)

nv.chord(G, group_by="continent", weight_by="flow")
```

Expected output: six arc segments (Africa, Asia, Europe, N. America, Oceania, S. America) with colored ribbons showing migration volumes. The USA-bound flows from Asia and N. America should produce the thickest ribbons.

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Group Arc Computation EARS](./arc-computation-EARS.md)
- [Edge Aggregation EARS](./edge-aggregation-EARS.md)
- [Chord Rendering EARS](./chord-rendering-EARS.md)
- [Chord API EARS](./chord-api-EARS.md)
