# API Integration - EARS

**Parent LLD**: ./LLD.md

## High-Level API

- [ ] **BKEND-API-001**: When `backend` is not specified, the system shall behave identically to the current matplotlib-only implementation.
- [ ] **BKEND-API-002**: When `backend="matplotlib"` is specified, the system shall produce identical output to the default (no-backend) behavior.
- [ ] **BKEND-API-003**: When `backend="plotly"` is specified, the system shall accept all parameters that the matplotlib backend accepts, with identical semantics.
- [ ] **BKEND-API-004**: When an unsupported backend value is provided, the system shall raise a `ValueError` listing available backends.
- [ ] **BKEND-API-005**: When `backend="plotly"` is specified and plotly is not installed, the system shall raise an `ImportError` with installation instructions.

## Parameter Propagation

- [ ] **BKEND-API-010**: The `backend` parameter shall be accepted by `api.base()` and `api.base_cloned()`.
- [ ] **BKEND-API-011**: The `backend` parameter shall be propagated to `nodes.draw()` and `edges.draw()`.
- [ ] **BKEND-API-012**: All existing plot partials (`api.circos`, `api.arc`, `api.hive`, `api.matrix`, `api.parallel`, `api.geo`) shall support the `backend` parameter.

## Mid-Level API

- [ ] **BKEND-API-020**: `nodes.draw()` shall accept an optional `backend` keyword argument.
- [ ] **BKEND-API-021**: `edges.draw()` shall accept an optional `backend` keyword argument.
- [ ] **BKEND-API-022**: When `backend` is `None` in mid-level functions, the system shall use the current matplotlib rendering path (backward compat).

## Annotations

- [ ] **BKEND-API-030**: Annotation functions shall accept either `matplotlib.axes.Axes` or `plotly.graph_objects.Figure` as the `ax` parameter.
- [ ] **BKEND-API-031**: When `ax` is a matplotlib Axes, annotations shall use matplotlib rendering.
- [ ] **BKEND-API-032**: When `ax` is a plotly Figure, annotations shall use plotly rendering.
- [ ] **BKEND-API-033**: When `ax` is `None`, the system shall default to `plt.gca()` (matplotlib behavior).

## Return Types

- [ ] **BKEND-API-040**: When `backend="matplotlib"`, the plot function shall return `matplotlib.axes.Axes`.
- [ ] **BKEND-API-041**: When `backend="plotly"`, the plot function shall return `plotly.graph_objects.Figure`.

## Related Documents

- [Multi-Backend LLD](./LLD.md)
