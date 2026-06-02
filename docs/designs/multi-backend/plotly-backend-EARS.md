# Plotly Backend - EARS

**Parent LLD**: ./LLD.md

## Setup and Configuration

- [ ] **BKEND-PLOTLY-001**: `create_axes` shall return a `plotly.graph_objects.Figure` object.
- [ ] **BKEND-PLOTLY-002**: `get_figure` shall return the same `go.Figure` object.
- [ ] **BKEND-PLOTLY-003**: The plotly backend shall be importable only when `plotly>=5.0` is installed.
- [ ] **BKEND-PLOTLY-004**: When plotly is not installed, `get_backend("plotly")` shall raise `ImportError` with pip install instructions.

## Plot Type Support

- [ ] **BKEND-PLOTLY-010**: The plotly backend shall support all six plot types: circos, arc, hive, matrix, parallel, geo.
- [ ] **BKEND-PLOTLY-011**: All encoding parameters (`node_color_by`, `edge_color_by`, `alpha_by`, `size_by`, `lw_by`) shall work with identical semantics to the matplotlib backend.
- [ ] **BKEND-PLOTLY-012**: Custom palettes (`node_palette`, `edge_palette`) shall be supported.

## Node Rendering

- [ ] **BKEND-PLOTLY-020**: `draw_nodes` shall add a `go.Scatter` trace with `mode='markers'` to the figure.
- [ ] **BKEND-PLOTLY-021**: Node colors shall be mapped to marker `color` property.
- [ ] **BKEND-PLOTLY-022**: Node sizes shall be mapped to marker `size` property (scaled for plotly pixel conventions).
- [ ] **BKEND-PLOTLY-023**: Node alphas shall be mapped to marker `opacity` property.
- [ ] **BKEND-PLOTLY-024**: Node hover text shall display the node label and all node attributes.

## Edge Rendering

- [ ] **BKEND-PLOTLY-030**: `draw_edges` shall use `nxviz.paths` for edge path coordinates.
- [ ] **BKEND-PLOTLY-031**: For circos, arc, hive, and parallel plots, edges shall be rendered as `go.Scatter` traces with `mode='lines'`.
- [ ] **BKEND-PLOTLY-032**: For matrix plots, edges shall be rendered as `go.Scatter` traces with `mode='markers'`.
- [ ] **BKEND-PLOTLY-033**: Edge colors shall be mapped to line `color` property.
- [ ] **BKEND-PLOTLY-034**: Edge line widths shall be mapped to line `width` property.
- [ ] **BKEND-PLOTLY-035**: Edge alphas shall be mapped to line `opacity` property.
- [ ] **BKEND-PLOTLY-036**: Edge hover text shall display source node, target node, and all edge attributes.

## Interactivity

- [ ] **BKEND-PLOTLY-040**: Hover tooltips shall be enabled by default showing node/edge attributes.
- [ ] **BKEND-PLOTLY-041**: Zoom and pan shall be enabled by default.
- [ ] **BKEND-PLOTLY-042**: The plotly figure shall be displayable in Jupyter notebooks via `.show()`.

## Axes Manipulation

- [ ] **BKEND-PLOTLY-050**: `despine` shall hide axis lines, ticks, and background grid.
- [ ] **BKEND-PLOTLY-051**: `set_aspect_equal` shall set `scaleanchor="x"` and `scaleratio=1` on the y-axis.
- [ ] **BKEND-PLOTLY-052**: `rescale` shall set appropriate x/y axis ranges based on node positions.

## Annotation Support

- [ ] **BKEND-PLOTLY-060**: Group labels (circos_group, arc_group, hive_group, parallel_group, matrix_group) shall be rendered as text annotations on the figure.
- [ ] **BKEND-PLOTLY-061**: Colormapping annotations shall render as plotly-native colorbars for continuous data and legends for categorical data.
- [ ] **BKEND-PLOTLY-062**: Matrix block annotations shall be rendered as semi-transparent rectangles (shapes).

## Related Documents

- [Multi-Backend LLD](./LLD.md)
