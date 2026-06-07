# Chord Rendering - EARS

**Parent LLD**: ./LLD.md

## Arc Rendering

- [ ] **CHORD-REND-001**: The backend shall draw each group as a thick colored arc segment between `start_angle` and `end_angle` at the specified `radius`.
- [ ] **CHORD-REND-002**: The arc band width (radial thickness) shall be configurable via a parameter with a default of 20 pixels.
- [ ] **CHORD-REND-003**: The arc color shall match the group color from the GroupArcs DataFrame.
- [ ] **CHORD-REND-004**: The matplotlib backend shall render arcs using matplotlib patches (Arc or line segments with thick linewidth).
- [ ] **CHORD-REND-005**: The plotly backend shall render arcs using plotly shapes or scatter traces.

## Ribbon Rendering

- [ ] **CHORD-REND-010**: The backend shall draw each ribbon as a filled polygon connecting two arc sub-bands through the center of the circle.
- [ ] **CHORD-REND-011**: Each ribbon shall be colored with the source group's color at a default alpha of 0.4.
- [ ] **CHORD-REND-012**: The ribbon alpha shall be configurable via a parameter.
- [ ] **CHORD-REND-013**: The matplotlib backend shall render ribbons using `matplotlib.patches.Polygon` or `PathPatch`.
- [ ] **CHORD-REND-014**: The plotly backend shall render ribbons using filled scatter traces.
- [ ] **CHORD-REND-015**: When source_group equals target_group (self-loop), the system shall render the ribbon as a loop that exits and re-enters the same arc.
- [ ] **CHORD-REND-016**: Each ribbon shall have a full-opacity border (line) in the source group's color, even when the fill is semi-transparent. This border provides visual separation between overlapping ribbons and preserves the directionality cue from the target-gap offset.
- [ ] **CHORD-REND-017**: On hover (interactive backends only), the hovered ribbon shall transition to full-opacity fill while other ribbons shall dim to near-transparent fill. Ribbon borders shall follow the same transition (full-opacity border on hovered, dimmed border on others) so that the "arrow of intent" — which end is attached vs detached — remains legible for the highlighted ribbon.
- [ ] **CHORD-REND-018**: The border shall NOT be implemented via Plotly's trace-level `opacity` property (which applies uniformly to fill and line, overriding per-channel alpha). Instead, fill and border transparency shall be controlled independently through RGBA color strings on `fillcolor` and `line.color`.
- [ ] **CHORD-REND-019**: Each ribbon trace shall store pre-computed color variants in its `meta` attribute: `default_fill`, `default_line`, `highlight_fill`, `highlight_line`, `dimmed_fill`, `dimmed_line`. This avoids recomputing colors during interaction.
- [ ] **CHORD-REND-020**: Hover highlighting shall be implemented via client-side JavaScript using Plotly.js's `plotly_hover` and `plotly_unhover` DOM events with `Plotly.restyle()`, NOT via Python-side `FigureWidget.on_hover()` callbacks. The `FigureWidget` approach requires an ipywidgets event bridge that is unavailable in marimo and most non-Jupyter rendering contexts.
- [ ] **CHORD-REND-021**: The public API shall expose `chord_hover_html(fig)` which accepts a `go.Figure` returned by `chord()` and returns a full HTML document (with Plotly.js loaded from CDN) containing an inline `<script>` that attaches hover/unhover listeners. In marimo notebooks, users display it via `mo.iframe(nv.chord_hover_html(fig), height="600px")` because `mo.Html()` does not execute inline `<script>` tags (browser innerHTML restriction).

## Ribbon Coordinate Computation

- [ ] **CHORD-REND-020**: For each group, the system shall subdivide its arc into two contiguous zones: source sub-bands (outgoing flows) followed by target sub-bands (incoming flows). Source and target sub-bands shall never overlap angularly on the same arc.
- [ ] **CHORD-REND-021**: Each arc's total angular extent shall be split proportionally between source and target zones based on total outgoing flow vs total incoming flow: `src_share = arc_extent × total_outgoing / (total_outgoing + total_incoming)`.
- [ ] **CHORD-REND-022**: Source sub-bands shall be allocated first (phase 1), then target sub-bands shall start where source sub-bands ended (phase 2), using a single tracker per arc to guarantee sequential non-overlapping placement.
- [ ] **CHORD-REND-023**: All sub-bands (source and target) shall fit within their arc's `[start_angle, end_angle]` boundary — no angular overflow.
- [ ] **CHORD-REND-024**: The `ribbon_coords()` function shall return a list of dicts, each containing: source_group, target_group, source_angle_start, source_angle_end, target_angle_start, target_angle_end, path_coords, color, alpha, weight.
- [ ] **CHORD-REND-025**: Path coordinates for each ribbon shall form a smooth Bezier curve through the center of the circle.
- [ ] **CHORD-REND-026**: The four edge points of each ribbon (source start, source end, target start, target end) shall lie on the circle at the specified radius.
- [ ] **CHORD-REND-027**: For self-loops (source_group == target_group), the source sub-band and target sub-band shall be adjacent on the same arc (source first, target following), with the ribbon path looping through the interior via a control radius of `inner_r × 0.5`.

## Arc Labels

- [ ] **CHORD-REND-030**: The backend shall draw group labels at the midpoint angle of each arc, positioned outside the circle.
- [ ] **CHORD-REND-031**: Labels shall be oriented radially (readable from outside the circle).
- [ ] **CHORD-REND-032**: The label radius shall be configurable, defaulting to `radius + padding`.

## Related Documents

- [Chord LLD](./LLD.md)
