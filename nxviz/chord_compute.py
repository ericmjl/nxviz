"""Compute-phase functions for chord diagram plots.

Chord diagrams aggregate nodes into arc segments and edges into ribbons,
showing aggregate flow between groups rather than individual connections.
"""

from typing import Dict, Hashable, List, Optional, Union

import numpy as np
import pandas as pd

from nxviz import encodings
from nxviz.polcart import to_cartesian


def group_arcs(
    nt: pd.DataFrame,
    group_by: Hashable,
    palette: Optional[Union[Dict, List]] = None,
    gap_fraction: float = 0.01,
) -> pd.DataFrame:
    """Compute arc segments for each group of nodes.

    Returns a DataFrame with one row per group containing angular extents
    and colors for rendering arc segments around a circle.

    Parameters
    ----------
    nt : pd.DataFrame
        Node table with group_by attribute as a column.
    group_by : Hashable
        Node attribute key for grouping.
    palette : optional
        Custom color palette for groups.
    gap_fraction : float
        Fraction of 2*pi to use as gap between each adjacent arc pair.
    """
    group_counts = nt.groupby(group_by).size().sort_index()
    groups = list(group_counts.index)
    n_groups = len(groups)

    if n_groups < 2:
        raise ValueError(
            f"Chord diagrams require at least 2 groups, got {n_groups}. "
            f"Groups found: {groups}"
        )

    total_nodes = group_counts.sum()
    gap_per_group = 2 * np.pi * gap_fraction
    total_gap = n_groups * gap_per_group
    available = 2 * np.pi - total_gap

    rows = []
    current_angle = gap_per_group / 2
    group_labels = pd.Series(groups, name=group_by)
    group_colors_series = encodings.data_color(group_labels, group_labels, palette)

    for i, (grp, count) in enumerate(group_counts.items()):
        extent = available * count / total_nodes
        rows.append(
            {
                "group": grp,
                "start_angle": current_angle,
                "end_angle": current_angle + extent,
                "n_nodes": count,
                "color": group_colors_series.iloc[i],
            }
        )
        current_angle += extent + gap_per_group

    return pd.DataFrame(rows)


def aggregate_edges(
    et: pd.DataFrame,
    nt: pd.DataFrame,
    group_by: Hashable,
    weight_by: Hashable = None,
) -> pd.DataFrame:
    """Aggregate edges by source group and target group.

    Parameters
    ----------
    et : pd.DataFrame
        Edge table with 'source' and 'target' columns.
    nt : pd.DataFrame
        Node table with group_by attribute as a column.
    group_by : Hashable
        Node attribute key for grouping.
    weight_by : Hashable, optional
        Edge attribute key for weight. If None, count edges.
    """
    node_to_group = nt[group_by].to_dict()

    if et.empty:
        return pd.DataFrame(columns=["source_group", "target_group", "weight"])

    et_copy = et.copy()
    et_copy["source_group"] = et_copy["source"].map(node_to_group)
    et_copy["target_group"] = et_copy["target"].map(node_to_group)

    missing_source = et_copy["source_group"].isna()
    missing_target = et_copy["target_group"].isna()
    if missing_source.any():
        missing_nodes = et_copy.loc[missing_source, "source"].unique().tolist()
        raise KeyError(f"Edge source nodes not found in node table: {missing_nodes}")
    if missing_target.any():
        missing_nodes = et_copy.loc[missing_target, "target"].unique().tolist()
        raise KeyError(f"Edge target nodes not found in node table: {missing_nodes}")

    if weight_by is not None:
        if weight_by not in et_copy.columns:
            raise KeyError(
                f"Edge attribute '{weight_by}' not found. "
                f"Available columns: {list(et_copy.columns)}"
            )
        agg = (
            et_copy.groupby(["source_group", "target_group"])[weight_by]
            .sum()
            .reset_index()
        )
        agg.columns = ["source_group", "target_group", "weight"]
    else:
        agg = (
            et_copy.groupby(["source_group", "target_group"])
            .size()
            .reset_index(name="weight")
        )

    return agg


def ribbon_coords(
    agg_edges: pd.DataFrame,
    group_arcs_df: pd.DataFrame,
    radius: float = 10.0,
    alpha: float = 0.4,
    arc_width: float = 0.05,
) -> List[Dict]:
    """Compute ribbon path coordinates between arc segments.

    Each group's arc is subdivided into bands proportional to outgoing flow.
    Ribbons are drawn as Bezier curves through the center connecting bands.

    Bands on each arc are allocated in group-order around the circle
    to prevent ribbons from crossing each other.

    Parameters
    ----------
    agg_edges : pd.DataFrame
        Aggregated edges with source_group, target_group, weight columns.
    group_arcs_df : pd.DataFrame
        Group arc extents from group_arcs().
    radius : float
        Circle radius for positioning arc segments.
    alpha : float
        Default transparency for ribbons.
    """
    arc_lookup = {row["group"]: row for _, row in group_arcs_df.iterrows()}

    group_order = list(group_arcs_df["group"])
    group_index = {g: i for i, g in enumerate(group_order)}

    outgoing_flow = {}
    for _, row in agg_edges.iterrows():
        sg = row["source_group"]
        outgoing_flow[sg] = outgoing_flow.get(sg, 0) + row["weight"]

    incoming_flow = {}
    for _, row in agg_edges.iterrows():
        tg = row["target_group"]
        incoming_flow[tg] = incoming_flow.get(tg, 0) + row["weight"]

    arc_flow_budget = {}
    for grp in group_order:
        arc = arc_lookup[grp]
        arc_extent = arc["end_angle"] - arc["start_angle"]
        total_out = outgoing_flow.get(grp, 0)
        total_in = incoming_flow.get(grp, 0)
        total_flow = total_out + total_in
        if total_flow == 0:
            arc_flow_budget[grp] = {"src_share": 0.0, "tgt_share": 0.0}
        else:
            arc_flow_budget[grp] = {
                "src_share": arc_extent * total_out / total_flow,
                "tgt_share": arc_extent * total_in / total_flow,
            }

    source_band_tracker = {grp: arc["start_angle"] for grp, arc in arc_lookup.items()}

    source_bands = {grp: [] for grp in group_order}
    for _, row in agg_edges.iterrows():
        sg = row["source_group"]
        source_bands[sg].append(row.to_dict())

    for grp in group_order:
        source_bands[grp].sort(key=lambda r: group_index.get(r["target_group"], 0))

    edge_records = []
    for grp in group_order:
        for edge_row in source_bands[grp]:
            sg = edge_row["source_group"]
            tg = edge_row["target_group"]
            weight = edge_row["weight"]

            src_arc = arc_lookup[sg]
            tgt_arc = arc_lookup[tg]

            src_total = outgoing_flow[sg]
            tgt_total = incoming_flow[tg]

            src_extent = (
                arc_flow_budget[sg]["src_share"] * weight / src_total
                if src_total > 0
                else 0
            )
            tgt_extent = (
                arc_flow_budget[tg]["tgt_share"] * weight / tgt_total
                if tgt_total > 0
                else 0
            )

            src_start = source_band_tracker[sg]
            src_end = src_start + src_extent
            source_band_tracker[sg] = src_end

            edge_records.append(
                {
                    "sg": sg,
                    "tg": tg,
                    "weight": weight,
                    "src_start": src_start,
                    "src_end": src_end,
                    "tgt_extent": tgt_extent,
                    "src_arc": src_arc,
                    "tgt_arc": tgt_arc,
                }
            )

    target_band_tracker = {grp: source_band_tracker[grp] for grp in group_order}

    ribbons = []
    n_curve = 50
    t = np.linspace(0, 1, n_curve)
    inner_r = radius * (1 - arc_width / 2)
    target_r = inner_r - 0.03 * radius

    for rec in edge_records:
        sg = rec["sg"]
        tg = rec["tg"]
        weight = rec["weight"]
        src_start = rec["src_start"]
        src_end = rec["src_end"]
        src_arc = rec["src_arc"]
        tgt_arc = rec["tgt_arc"]

        tgt_start = target_band_tracker[tg]
        tgt_end = tgt_start + rec["tgt_extent"]
        target_band_tracker[tg] = tgt_end

        if sg == tg:
            ribbon_path = _self_loop_path(
                src_start, src_end, tgt_start, tgt_end, radius, inner_r, target_r, t
            )
        else:
            p_src_start = np.array(to_cartesian(inner_r, src_start))
            p_src_end = np.array(to_cartesian(inner_r, src_end))
            p_tgt_start = np.array(to_cartesian(target_r, tgt_start))
            p_tgt_end = np.array(to_cartesian(target_r, tgt_end))

            origin = np.array([0.0, 0.0])

            n_arc_src = max(int(abs(src_end - src_start) * 20), 3)
            src_thetas = np.linspace(src_start, src_end, n_arc_src)
            arc_src = np.column_stack(
                [
                    inner_r * np.cos(src_thetas),
                    inner_r * np.sin(src_thetas),
                ]
            )

            edge_top = _cubic_bezier(p_src_end, origin, p_tgt_start, t)

            n_arc_tgt = max(int(abs(tgt_end - tgt_start) * 20), 3)
            tgt_thetas = np.linspace(tgt_start, tgt_end, n_arc_tgt)
            arc_tgt = np.column_stack(
                [
                    target_r * np.cos(tgt_thetas),
                    target_r * np.sin(tgt_thetas),
                ]
            )

            edge_bot = _cubic_bezier(p_tgt_end, origin, p_src_start, t)

            ribbon_path = np.vstack([arc_src, edge_top, arc_tgt, edge_bot])

        color = src_arc["color"]

        ribbons.append(
            {
                "source_group": sg,
                "target_group": tg,
                "source_angle_start": src_start,
                "source_angle_end": src_end,
                "target_angle_start": tgt_start,
                "target_angle_end": tgt_end,
                "path_coords": ribbon_path,
                "color": color,
                "alpha": alpha,
                "weight": weight,
            }
        )

    return ribbons


def _ribbon_control(p1, p2):
    """Control point for a quadratic Bezier ribbon edge.

    The control point is the midpoint of p1 and p2, scaled toward the origin
    so the ribbon curves inward but the two edges don't converge at (0,0).
    """
    mid = (p1 + p2) / 2
    return mid * 0.5


def _cubic_bezier(start, control, end, t):
    """Evaluate quadratic Bezier from start through control to end."""
    result = np.zeros((len(t), 2))
    for i, ti in enumerate(t):
        result[i] = (1 - ti) ** 2 * start + 2 * (1 - ti) * ti * control + ti**2 * end
    return result


def _self_loop_path(
    src_start, src_end, tgt_start, tgt_end, radius, inner_r, target_r, t
):
    loop_r = inner_r * 0.5
    n_arc_src = max(int(abs(src_end - src_start) * 20), 3)
    src_thetas = np.linspace(src_start, src_end, n_arc_src)
    arc_src = np.column_stack(
        [
            inner_r * np.cos(src_thetas),
            inner_r * np.sin(src_thetas),
        ]
    )
    n_arc_tgt = max(int(abs(tgt_end - tgt_start) * 20), 3)
    tgt_thetas = np.linspace(tgt_start, tgt_end, n_arc_tgt)
    arc_tgt = np.column_stack(
        [
            target_r * np.cos(tgt_thetas),
            target_r * np.sin(tgt_thetas),
        ]
    )
    mid_out = (src_end + tgt_start) / 2
    mid_back = (tgt_end + src_start) / 2
    edge_out = _cubic_bezier(
        np.array(to_cartesian(inner_r, src_end)),
        np.array(to_cartesian(loop_r, mid_out)),
        np.array(to_cartesian(target_r, tgt_start)),
        t,
    )
    edge_back = _cubic_bezier(
        np.array(to_cartesian(target_r, tgt_end)),
        np.array(to_cartesian(loop_r, mid_back)),
        np.array(to_cartesian(inner_r, src_start)),
        t,
    )
    return np.vstack([arc_src, edge_out, arc_tgt, edge_back])
