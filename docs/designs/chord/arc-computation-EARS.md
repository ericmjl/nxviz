# Group Arc Computation - EARS

**Parent LLD**: ./LLD.md

## Arc Sizing

- [ ] **CHORD-ARC-001**: The system shall assign each group an angular extent proportional to its node count relative to total nodes.
- [ ] **CHORD-ARC-002**: The system shall place a configurable angular gap (default 2π × 0.01 radians per gap) between adjacent arcs.
- [ ] **CHORD-ARC-003**: The system shall compute `start_angle` and `end_angle` for each group such that all arcs plus gaps sum to exactly 2π radians.
- [ ] **CHORD-ARC-004**: When `sort_by` is provided, the system shall order groups by the specified node attribute's sorted values within each group.
- [ ] **CHORD-ARC-005**: When `sort_by` is not provided, the system shall order groups alphabetically by group label.

## Arc Coloring

- [ ] **CHORD-ARC-010**: The system shall assign each group a distinct color using the existing `encodings.color_func()` pipeline.
- [ ] **CHORD-ARC-011**: When `node_palette` is provided, the system shall use it as the color mapping for group labels.
- [ ] **CHORD-ARC-012**: The system shall return colors as RGBA tuples in the GroupArcs DataFrame.

## Output Contract

- [ ] **CHORD-ARC-020**: The `group_arcs()` function shall return a pandas DataFrame with columns: group, start_angle, end_angle, n_nodes, color.
- [ ] **CHORD-ARC-021**: Each group shall appear exactly once in the output.
- [ ] **CHORD-ARC-022**: The sum of all `(end_angle - start_angle)` values shall equal `2π - (n_groups × gap_per_group)`.

## Edge Cases

- [ ] **CHORD-ARC-030**: If there is only one group, the system shall assign it the full circle minus one gap.
- [ ] **CHORD-ARC-031**: If a group has zero nodes after filtering, the system shall raise a ValueError.

## Related Documents

- [Chord LLD](./LLD.md)
