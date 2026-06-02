# Multi-Backend Support - Low-Level Design

**Created**: 2026-06-02
**HLD Link**: ../../high-level-design.md

## Overview

This feature adds a backend abstraction layer to nxviz that separates the compute phase (layouts, encodings, geometry) from the render phase (drawing patches, annotations, axes manipulation). The `PlotBackend` protocol defines the render interface. The existing matplotlib rendering is extracted into `MatplotlibBackend`, and a new `PlotlyBackend` provides interactive web plots. Users switch backends by adding `backend="plotly"` to their existing API calls.

## Component Overview

### New Modules

| Module | Responsibility |
|--------|---------------|
| `nxviz/paths.py` | Backend-agnostic edge path coordinate computation (extracted from `lines.py`) |
| `nxviz/backend.py` | `PlotBackend` protocol definition + `get_backend()` factory |
| `nxviz/backends/__init__.py` | Backend registry |
| `nxviz/backends/matplotlib_backend.py` | Matplotlib implementation of `PlotBackend` |
| `nxviz/backends/plotly_backend.py` | Plotly implementation of `PlotBackend` |

### Modified Modules

| Module | Change |
|--------|--------|
| `nxviz/lines.py` | Calls `paths.py` internally, wraps in matplotlib patches |
| `nxviz/nodes.py` | Accepts optional `backend` kwarg in `draw()` |
| `nxviz/edges.py` | Accepts optional `backend` kwarg in `draw()` |
| `nxviz/api.py` | Adds `backend="matplotlib"` parameter to `base()` and `base_cloned()` |
| `nxviz/annotate.py` | Auto-detects backend from axes/figure type |
| `pyproject.toml` | Adds `plotly` optional extra |

## Data Flow

### Current flow (matplotlib only):

```
api.base(G, ...)
  ├── nodes.draw(G, layout_func, ...) → pos  [creates Circle patches, ax.add_patch()]
  ├── edges.draw(G, pos, lines_func, ...)     [creates PathPatch, ax.add_patch()]
  ├── plots.despine()
  ├── plots.aspect_equal()
  └── return plt.gca()
```

### New flow (with backend):

```
api.base(G, ..., backend="plotly")
  ├── backend = get_backend("plotly")
  ├── axes = backend.create_axes()
  │
  ├── COMPUTE (unchanged):
  │   ├── utils.node_table(G) → nt
  │   ├── layouts.circos(nt, ...) → pos
  │   ├── nodes.node_colors(nt, ...) → colors
  │   ├── nodes.transparency(nt, ...) → alphas
  │   ├── nodes.node_size(nt, ...) → sizes
  │   ├── utils.edge_table(G) → et
  │   ├── edges.edge_colors(et, ...) → edge_colors
  │   ├── edges.line_width(et, ...) → lw
  │   ├── edges.transparency(et, ...) → edge_alphas
  │   └── paths.circos_coords(et, pos) → edge_path_coords
  │
  ├── RENDER (delegated):
  │   ├── backend.draw_nodes(axes, nt, pos, colors, alphas, sizes)
  │   ├── backend.draw_edges(axes, et, pos, edge_path_coords, edge_colors, edge_alphas, lw, "circos")
  │   ├── backend.despine(axes)
  │   ├── backend.set_aspect_equal(axes)
  │   └── backend.rescale(axes, pos, "circos")
  │
  └── return backend.get_figure(axes)
```

### Backward compatibility path (backend=None, default):

When `backend` is not specified or is `"matplotlib"`, the code follows the current path through `nodes.draw()` and `edges.draw()` which internally call matplotlib directly. The `MatplotlibBackend` wraps the same code, so output is identical.

## PlotBackend Protocol

```python
class PlotBackend(Protocol):
    def create_axes(self) -> Any: ...
    def draw_nodes(self, axes, nt, pos, colors, alphas, sizes, **kw) -> None: ...
    def draw_edges(self, axes, et, pos, path_coords, colors, alphas, lw, line_type, pos_cloned=None, **kw) -> None: ...
    def despine(self, axes) -> None: ...
    def set_aspect_equal(self, axes) -> None: ...
    def rescale(self, axes, G, plot_type) -> None: ...
    def get_figure(self, axes) -> Any: ...
```

## Annotation Auto-Detection

Annotation functions accept an `ax` parameter (already the case). The auto-detection logic:

```python
def _get_backend_for_axes(ax):
    import matplotlib.axes
    if ax is None:
        ax = plt.gca()
    if isinstance(ax, matplotlib.axes.Axes):
        return get_backend("matplotlib")
    # Assume plotly Figure
    return get_backend("plotly")
```

Each annotation function delegates to the backend's annotation methods.

## Edge Path Coordinate Extraction

### `nxviz/paths.py` Functions

Each function returns a list of numpy arrays. Each array is shape (N, 2) representing (x, y) control points.

| Function | Returns | Notes |
|----------|---------|-------|
| `circos_coords(et, pos)` | `List[np.ndarray]` | 3-point Bezier through (0,0) |
| `line_coords(et, pos)` | `List[np.ndarray]` | 2-point straight lines |
| `arc_coords(et, pos)` | `List[np.ndarray]` | Sampled arc points (discretized) |
| `hive_coords(et, pos, pos_cloned, curves)` | `List[np.ndarray]` | 4-point or 2-point curves |
| `matrix_coords(et, pos, pos_cloned)` | `List[Tuple[float, float]]` | Single (x,y) center points |

## Error Handling

| Condition | Error | Message |
|-----------|-------|---------|
| Unknown backend name | `ValueError` | "Unknown backend 'X'. Available: matplotlib, plotly" |
| Plotly not installed | `ImportError` | "Plotly backend requires plotly. Install with: pip install nxviz[plotly]" |
| Backend missing method | `AttributeError` | Caught by Protocol enforcement |

## Dependencies

| Package | Version | Required |
|---------|---------|----------|
| matplotlib | >=3.3.3 | Core (always) |
| plotly | >=5.0 | Optional (`pip install nxviz[plotly]`) |

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Backend Protocol EARS](./backend-protocol-EARS.md)
- [Matplotlib Backend EARS](./matplotlib-backend-EARS.md)
- [Plotly Backend EARS](./plotly-backend-EARS.md)
- [Edge Paths EARS](./edge-paths-EARS.md)
- [API Integration EARS](./api-integration-EARS.md)
