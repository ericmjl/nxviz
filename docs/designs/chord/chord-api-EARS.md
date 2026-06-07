# Chord API - EARS

**Parent LLD**: ./LLD.md

## Function Signature

- [ ] **CHORD-API-001**: The `nv.chord()` function shall accept a NetworkX graph as its first argument.
- [ ] **CHORD-API-002**: The `nv.chord()` function shall accept `group_by` as a required keyword argument specifying the node attribute for grouping.
- [ ] **CHORD-API-003**: The `nv.chord()` function shall accept `weight_by` as an optional keyword argument specifying the edge attribute for flow weight.
- [ ] **CHORD-API-004**: The `nv.chord()` function shall accept `sort_by` as an optional keyword argument controlling group ordering.
- [ ] **CHORD-API-005**: The `nv.chord()` function shall accept `node_palette` and `edge_palette` as optional keyword arguments for custom color mapping.
- [ ] **CHORD-API-006**: The `nv.chord()` function shall accept `backend` as a keyword argument with default `"matplotlib"`.
- [ ] **CHORD-API-007**: The `nv.chord()` function shall accept `alpha` as a keyword argument controlling ribbon transparency (default 0.4).
- [ ] **CHORD-API-008**: The `nv.chord()` function shall accept `arc_width` as a keyword argument controlling the radial thickness of arcs (default 20).

## Return Value

- [ ] **CHORD-API-010**: When `backend="matplotlib"`, the function shall return a `matplotlib.axes.Axes` object.
- [ ] **CHORD-API-011**: When `backend="plotly"`, the function shall return a `plotly.graph_objects.Figure` object.

## Export

- [ ] **CHORD-API-020**: The `chord` function shall be importable as `nxviz.chord` and `nxviz.api.chord`.
- [ ] **CHORD-API-021**: The `chord` function shall appear in `nxviz.__all__` if it is defined.

## Error Handling

- [ ] **CHORD-API-030**: When `group_by` is None, the system shall raise a TypeError with message indicating `group_by` is required for chord diagrams.
- [ ] **CHORD-API-031**: When the graph has fewer than 2 groups, the system shall raise a ValueError with message indicating chord diagrams require at least 2 groups.
- [ ] **CHORD-API-032**: When `weight_by` refers to an edge attribute that does not exist on all edges, the system shall raise a KeyError naming the missing attribute.

## Backend Dispatch

- [ ] **CHORD-API-040**: When `backend="matplotlib"`, the function shall use the matplotlib rendering path directly.
- [ ] **CHORD-API-041**: When `backend` is not `"matplotlib"`, the function shall use `get_backend(backend)` to obtain a backend instance and call its chord-specific methods.

## Related Documents

- [Chord LLD](./LLD.md)
