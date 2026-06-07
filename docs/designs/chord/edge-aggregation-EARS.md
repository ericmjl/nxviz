# Edge Aggregation - EARS

**Parent LLD**: ./LLD.md

## Group Mapping

- [ ] **CHORD-AGG-001**: The system shall build a node-to-group mapping from the node table using the `group_by` attribute.
- [ ] **CHORD-AGG-002**: The system shall map each edge's source node to its group via the node-to-group mapping.
- [ ] **CHORD-AGG-003**: The system shall map each edge's target node to its group via the node-to-group mapping.

## Weight Aggregation

- [ ] **CHORD-AGG-010**: When `weight_by` is provided, the system shall sum the specified edge attribute for all edges sharing the same (source_group, target_group) pair.
- [ ] **CHORD-AGG-011**: When `weight_by` is not provided, the system shall count the number of edges for each (source_group, target_group) pair.
- [ ] **CHORD-AGG-012**: For directed graphs, the system shall preserve source→target directionality in the aggregation.
- [ ] **CHORD-AGG-013**: For undirected graphs, the system shall aggregate both (A→B) and (B→A) directions as separate rows (matching existing `edge_table` behavior which duplicates undirected edges).

## Self-Loops

- [ ] **CHORD-AGG-020**: When source_group equals target_group, the system shall include the aggregated edge as a self-loop row.

## Output Contract

- [ ] **CHORD-AGG-030**: The `aggregate_edges()` function shall return a pandas DataFrame with columns: source_group, target_group, weight.
- [ ] **CHORD-AGG-031**: Each unique (source_group, target_group) pair shall appear exactly once in the output.
- [ ] **CHORD-AGG-032**: All weight values shall be non-negative floats or integers.

## Edge Cases

- [ ] **CHORD-AGG-040**: If an edge references a node not in the node table, the system shall raise a KeyError.
- [ ] **CHORD-AGG-041**: If there are no edges, the system shall return an empty DataFrame with the correct columns.

## Related Documents

- [Chord LLD](./LLD.md)
