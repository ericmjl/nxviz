# Matplotlib Backend - EARS

**Parent LLD**: ./LLD.md

## Backward Compatibility

- [ ] **BKEND-MPL-001**: When `backend` is not specified, the system shall behave identically to the pre-backend implementation.
- [ ] **BKEND-MPL-002**: The matplotlib backend shall return a `matplotlib.axes.Axes` object from `get_figure()`.
- [ ] **BKEND-MPL-003**: The matplotlib backend shall produce pixel-exact output for all existing test cases.

## Node Rendering

- [ ] **BKEND-MPL-010**: `draw_nodes` shall create `matplotlib.patches.Circle` objects for each node.
- [ ] **BKEND-MPL-011**: `draw_nodes` shall set face color, alpha, radius, and zorder from the provided encoding Series.
- [ ] **BKEND-MPL-012**: `draw_nodes` shall pass through extra `encodings_kwargs` to the Circle constructor.

## Edge Rendering

- [ ] **BKEND-MPL-020**: `draw_edges` shall use `nxviz.lines` functions to create `PathPatch` objects for circos, arc, hive, and straight line plots.
- [ ] **BKEND-MPL-021**: `draw_edges` shall create `Circle` patches for matrix plot edges.
- [ ] **BKEND-MPL-022**: `draw_edges` shall handle `pos_cloned` for hive and matrix plots.

## Axes Manipulation

- [ ] **BKEND-MPL-030**: `despine` shall remove all spines and hide x/y axis ticks.
- [ ] **BKEND-MPL-031**: `set_aspect_equal` shall set aspect ratio to "equal".
- [ ] **BKEND-MPL-032**: `rescale` shall call `relim()` and `autoscale_view()` for default plots.
- [ ] **BKEND-MPL-033**: `rescale` shall use `rescale_arc` for arc plots and `rescale_square` for hive plots.

## Related Documents

- [Multi-Backend LLD](./LLD.md)
