# Edge Paths - EARS

**Parent LLD**: ./LLD.md

## Path Extraction

- [ ] **BKEND-PATH-001**: The system shall provide a `nxviz.paths` module with backend-agnostic edge path coordinate functions.
- [ ] **BKEND-PATH-002**: `circos_coords(et, pos)` shall return a list of numpy arrays, each shape (3, 2), representing the source, center (0,0), and target control points for each edge.
- [ ] **BKEND-PATH-003**: `line_coords(et, pos)` shall return a list of numpy arrays, each shape (2, 2), representing source and target points for straight edges.
- [ ] **BKEND-PATH-004**: `arc_coords(et, pos, n_points)` shall return a list of numpy arrays, each shape (n_points, 2), representing discretized arc curve points for each edge.
- [ ] **BKEND-PATH-005**: `hive_coords(et, pos, pos_cloned, curves)` shall return a list of numpy arrays, each shape (4, 2) when curves=True or (2, 2) when curves=False.
- [ ] **BKEND-PATH-006**: `matrix_coords(et, pos, pos_cloned)` shall return a list of (x, y) tuples representing the center position of each edge dot.

## Backward Compatibility

- [ ] **BKEND-PATH-010**: `nxviz.lines.circos` shall call `paths.circos_coords` internally and wrap the result in matplotlib `PathPatch`.
- [ ] **BKEND-PATH-011**: `nxviz.lines.line` shall call `paths.line_coords` internally and wrap the result in matplotlib `PathPatch`.
- [ ] **BKEND-PATH-012**: `nxviz.lines.arc` shall continue using matplotlib `Arc` patches directly (not discretized) for matplotlib rendering.
- [ ] **BKEND-PATH-013**: `nxviz.lines.hive` shall call `paths.hive_coords` internally and wrap the result in matplotlib `PathPatch`.
- [ ] **BKEND-PATH-014**: `nxviz.lines.matrix` shall continue using matplotlib `Circle` patches directly.

## Related Documents

- [Multi-Backend LLD](./LLD.md)
