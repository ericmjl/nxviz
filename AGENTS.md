# nxviz - Agent Instructions

## Project Overview

nxviz is a Python library for rational network visualizations built on a grammar of graphics. It provides six plot types (circos, arc, hive, matrix, parallel, geo) through a functional API, with matplotlib as the default backend and optional interactive backends (plotly).

## Codebase Structure

```
nxviz/
├── __init__.py          # Public API exports
├── api.py               # High-level functional API (circos, arc, hive, etc.)
├── backend.py           # PlotBackend protocol + get_backend() factory
├── nodes.py             # Node drawing pipeline (layout → encode → glyph)
├── edges.py             # Edge drawing pipeline (encode → render)
├── layouts.py           # Pure position computation (returns pos dict)
├── encodings.py         # Data → visual property mapping (color, size, alpha)
├── lines.py             # Matplotlib patch generators for edges
├── paths.py             # Backend-agnostic edge path coordinate computation
├── plots.py             # Axes utilities (despine, aspect_equal, rescale)
├── annotate.py          # Text/colorbar/legend annotations
├── highlights.py        # Per-element highlight overlays
├── geometry.py          # Geometric helpers (circos_radius, item_theta)
├── polcart.py           # Polar ↔ Cartesian conversions
├── utils.py             # Data utilities (node_table, edge_table, group_and_sort)
├── io.py                # Deprecated dataframe-to-graph builder
├── facet.py             # Faceted (multi-panel) plot generation
└── backends/
    ├── __init__.py
    ├── matplotlib_backend.py   # Matplotlib rendering
    └── plotly_backend.py       # Plotly interactive rendering
```

## Architecture: Two Phases

1. **Compute phase** (backend-agnostic): `layouts`, `encodings`, `geometry`, `polcart`, `utils` produce positions, visual encodings, and path coordinates. No rendering code here.
2. **Render phase** (backend-specific): A `PlotBackend` draws nodes, edges, and annotations onto its native canvas.

The `backend="matplotlib"` default preserves the original code path exactly.

## Running Commands

**Use `pixi run`, not `uv run`.**

```bash
pixi run test          # Run tests
pixi run lint          # Run linters
pixi run build-docs    # Build docs
pixi run serve-docs    # Serve docs locally
```

The `tests` environment includes plotly for backend tests. To install the pixi environment:

```bash
pixi install
```

## Coding Standards

### No underscore-prefixed private methods

Do not use `_private_method` naming. All functions and methods are public. Use descriptive names instead:

```python
# Bad
def _resolve_layout(func):
    ...

# Good
def resolve_layout(func):
    ...
```

This applies to module-level functions, class methods, and helper functions equally.

### No comments in code

Do not add comments unless explicitly asked. Code should be self-documenting through clear naming.

### Code style

- Line length: 88 (ruff default)
- Quote style: double quotes
- Python: >=3.12
- Formatting and linting: ruff

### Testing

- Test framework: pytest
- Tests live in `tests/`
- Graph fixtures in `tests/fixtures/graphs.py`
- Run with: `pixi run test`
- **No mocking.** Do not use `unittest.mock`, `pytest.mock`, `patch`, `MagicMock`, or any mocking library. Use real objects, real graphs, and real function calls. If a dependency is heavy, create a lightweight fixture instead of mocking it.

### Backend system

- New backends implement the `PlotBackend` protocol from `nxviz.backend`
- Register in `BACKEND_REGISTRY` in `nxviz/backend.py`
- Optional dependencies go in `[project.optional-dependencies]` in `pyproject.toml`
- Lazy imports: backend modules are only loaded when `get_backend(name)` is called

### Dependency management

- Core deps (matplotlib, networkx, numpy, pandas, palettable, seaborn) stay in `[project.dependencies]`
- Optional deps (plotly) go in `[project.optional-dependencies]` as extras
- pixi features handle dev/test/doc tooling
