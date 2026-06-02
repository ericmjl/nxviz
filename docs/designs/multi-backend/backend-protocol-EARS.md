# Backend Protocol - EARS

**Parent LLD**: ./LLD.md

## Protocol Definition

- [ ] **BKEND-PROTO-001**: The system shall define a `PlotBackend` protocol with methods: `create_axes`, `draw_nodes`, `draw_edges`, `despine`, `set_aspect_equal`, `rescale`, `get_figure`.
- [ ] **BKEND-PROTO-002**: The system shall provide a `get_backend(name)` factory function that returns a `PlotBackend` instance for the given name.
- [ ] **BKEND-PROTO-003**: When `get_backend` is called with an unknown name, the system shall raise a `ValueError` listing available backends.
- [ ] **BKEND-PROTO-004**: The system shall register backends in a `BACKEND_REGISTRY` mapping names to import paths.
- [ ] **BKEND-PROTO-005**: When a backend's required package is not installed, the system shall raise an `ImportError` with installation instructions.
- [ ] **BKEND-PROTO-006**: Backend imports shall be lazy — the backend module is only imported when `get_backend()` is called for that name.

## Method Contracts

- [ ] **BKEND-PROTO-010**: `create_axes()` shall return a backend-specific axes/figure object.
- [ ] **BKEND-PROTO-011**: `draw_nodes(axes, nt, pos, colors, alphas, sizes, **kw)` shall render all nodes and return `None`.
- [ ] **BKEND-PROTO-012**: `draw_edges(axes, et, pos, path_coords, colors, alphas, lw, line_type, pos_cloned=None, **kw)` shall render all edges and return `None`.
- [ ] **BKEND-PROTO-013**: `despine(axes)` shall remove axis spines and tick marks.
- [ ] **BKEND-PROTO-014**: `set_aspect_equal(axes)` shall set equal aspect ratio on the axes.
- [ ] **BKEND-PROTO-015**: `rescale(axes, G, plot_type)` shall adjust axis limits to fit the plot.
- [ ] **BKEND-PROTO-016**: `get_figure(axes)` shall return the top-level figure object for the backend.

## Related Documents

- [Multi-Backend LLD](./LLD.md)
