# nxviz Multi-Backend Support - High-Level Design

**Created**: 2026-06-02

## Problem Statement

nxviz currently only supports matplotlib as a visualization backend. All plots are static images with no interactivity. Network visualizations especially benefit from hover tooltips, zoom/pan, click selection, and web deployment. Users need interactive plots for exploring dense graphs in Jupyter notebooks, dashboards, and standalone web applications.

## Goals

1. **Single-line backend switch**: Users switch between static and interactive backends by adding exactly one parameter (`backend="plotly"`) to their existing code. All other parameters remain identical.
2. **Backward compatibility**: The default matplotlib backend produces identical output to the current implementation.
3. **Interactive web backend**: Plotly as the first alternative backend, providing hover tooltips, zoom, pan, and web deployment out of the box.
4. **Extensible architecture**: A clean backend protocol that makes it straightforward to add Bokeh, Altair, or other backends in the future.

## Non-Goals

- Bokeh, Altair/Vega-Lite, or Holoviews backends in this version.
- Jupyter widget integration beyond what Plotly provides natively.
- Standalone HTML export as a separate feature (Plotly handles this natively).
- Modifying the existing grammar-of-graphics compute pipeline (layouts, encodings, geometry).
- Changing the mid-level or low-level API signatures for existing matplotlib usage.

## Target Users

- **Jupyter notebook users**: Want interactive hover/zoom to explore dense graphs without cluttering static plots.
- **Dashboard builders**: Need embeddable plots for Streamlit, Dash, or Panel apps.
- **Web developers**: Want standalone HTML outputs for sharing network visualizations.
- **Existing nxviz users**: Want zero-cost migration — same code, just add `backend="plotly"`.

## Architecture Overview

```
User Call: nv.circos(G, group_by="group", backend="plotly")
    │
    ▼
┌─────────────────── COMPUTE PHASE (backend-agnostic) ───────────────────┐
│                                                                        │
│  utils.node_table(G)  →  layouts.circos(nt, ...)  →  pos: Dict       │
│  utils.edge_table(G)  →  encodings.data_color(...)  →  colors: Series │
│                          encodings.data_size(...)   →  sizes: Series  │
│                          encodings.data_transparency(...) → alphas     │
│                          paths.circos_coords(...)  →  edge_coords     │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────── RENDER PHASE (backend-specific) ───────────────────┐
│                                                                        │
│  backend.draw_nodes(axes, nt, pos, colors, alphas, sizes)             │
│  backend.draw_edges(axes, et, pos, edge_coords, colors, alphas, lw)   │
│  backend.despine(axes)                                                 │
│  backend.set_aspect_equal(axes)                                        │
│  backend.rescale(axes, pos_data)                                       │
│  return backend.get_figure(axes)                                       │
│                                                                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌───────────────────────┐  │
│  │ MatplotlibBackend│  │  PlotlyBackend   │  │ FutureBackend (TBD)  │  │
│  │ → Axes           │  │  → go.Figure     │  │                      │  │
│  └─────────────────┘  └─────────────────┘  └───────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

The compute phase uses existing modules (layouts, encodings, geometry, polcart, utils) untouched. The render phase delegates to a `PlotBackend` implementation.

## Key Design Decisions

### Decision 1: Plotly as first web backend

**Choice**: Plotly
**Rationale**: Most popular interactive Python plotting library. Built-in hover/zoom/pan, great Jupyter integration, easy web deployment, well-maintained. Strong network graph support.

### Decision 2: Integrated in core package

**Choice**: Backend protocol + matplotlib in core, plotly as optional extra (`pip install nxviz[plotly]`).
**Rationale**: Simpler for users than a separate package. Lazy imports ensure core stays lightweight. The `nxviz.backends` namespace is reserved for future backends.

### Decision 3: Return type varies by backend

**Choice**: matplotlib returns `matplotlib.axes.Axes`, plotly returns `plotly.graph_objects.Figure`.
**Rationale**: Each backend returns its native object type, matching Python ecosystem conventions. Users call `.show()` or `.savefig()` as appropriate.

### Decision 4: Annotations auto-detect backend

**Choice**: Annotation functions accept either `matplotlib.axes.Axes` or `plotly.graph_objects.Figure` and dispatch via `isinstance`.
**Rationale**: Users pass the object returned by the plot call. No extra `backend=` parameter needed on annotations.

### Decision 5: Extract path computation from lines.py

**Choice**: New `nxviz/paths.py` module with backend-agnostic coordinate computation. `lines.py` calls `paths.py` then wraps in matplotlib patches.
**Rationale**: Edge path coordinates (Bezier curves, arcs, straight lines) are mathematical, not rendering-specific. Separating them enables any backend to use the same curves.

### Decision 6: Full annotation parity in v1

**Choice**: Group labels, colormaps, legends all work with Plotly on day one.
**Rationale**: Annotations are essential for readability. Shipping without them would make the Plotly backend feel incomplete.

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Feature parity gaps between backends | Plotly backend tested against all 6 plot types with all encoding parameters |
| Breaking existing matplotlib behavior | Pixel-exact output verified by running existing test suite unchanged |
| Plotly dependency bloat | Optional extra with lazy import; clear error message if not installed |
| Maintenance burden of multiple backends | Clean protocol boundary limits cross-backend coupling |
| Performance for large graphs with Plotly | Group edges into single traces where possible; document performance tips |

## Related Designs

- [Multi-Backend LLD](./designs/multi-backend/LLD.md)
- [Chord Diagram LLD](./designs/chord/LLD.md)
