"""Plotly backend for nxviz.

Provides interactive web-based network visualizations using Plotly.
Requires plotly>=5.0 to be installed (pip install nxviz[plotly]).
"""

from typing import Any, Dict, Hashable, List, Optional, Tuple

import numpy as np
import pandas as pd

try:
    import plotly.graph_objects as go
except ImportError:
    raise ImportError(
        "The 'plotly' backend requires plotly. "
        "Install it with: pip install nxviz[plotly]"
    )


def rgba_to_plotly_str(color) -> str:
    """Convert an RGBA tuple to a plotly-compatible color string."""
    if isinstance(color, str):
        return color
    if isinstance(color, (tuple, list, np.ndarray)):
        if len(color) == 4:
            r, g, b = [int(c * 255) if c <= 1 else int(c) for c in color[:3]]
            a = color[3]
            return f"rgba({r},{g},{b},{a})"
        elif len(color) == 3:
            r, g, b = [int(c * 255) if c <= 1 else int(c) for c in color]
            return f"rgb({r},{g},{b})"
    return str(color)


def node_hover_text(nt: pd.DataFrame) -> pd.Series:
    """Generate hover text for each node showing all attributes."""
    texts = []
    for node, row in nt.iterrows():
        parts = [f"<b>{node}</b>"]
        for col, val in row.items():
            parts.append(f"{col}: {val}")
        texts.append("<br>".join(parts))
    return pd.Series(texts, index=nt.index)


def edge_hover_text(et: pd.DataFrame) -> pd.Series:
    """Generate hover text for each edge showing all attributes."""
    texts = []
    for _, row in et.iterrows():
        parts = [f"<b>{row['source']} → {row['target']}</b>"]
        for col, val in row.items():
            if col not in ("source", "target"):
                parts.append(f"{col}: {val}")
        texts.append("<br>".join(parts))
    return pd.Series(texts, index=et.index)


def bezier_curve(points: np.ndarray, n_points: int = 50) -> np.ndarray:
    """Evaluate a Bezier curve at n_points given control points.

    Supports quadratic (3 points) and cubic (4 points) Bezier curves.
    """
    n_control = len(points)
    t = np.linspace(0, 1, n_points)

    if n_control == 2:
        result = np.outer(1 - t, points[0]) + np.outer(t, points[1])
    elif n_control == 3:
        result = (
            np.outer((1 - t) ** 2, points[0])
            + np.outer(2 * (1 - t) * t, points[1])
            + np.outer(t**2, points[2])
        )
    elif n_control == 4:
        result = (
            np.outer((1 - t) ** 3, points[0])
            + np.outer(3 * (1 - t) ** 2 * t, points[1])
            + np.outer(3 * (1 - t) * t**2, points[2])
            + np.outer(t**3, points[3])
        )
    else:
        result = points

    return result


class PlotlyBackend:
    """Plotly-based rendering backend for interactive network visualizations."""

    def create_axes(self) -> go.Figure:
        """Create and return a Plotly Figure."""
        fig = go.Figure()
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
        )
        return fig

    def draw_nodes(
        self,
        axes: go.Figure,
        nt: pd.DataFrame,
        pos: Dict[Hashable, np.ndarray],
        colors: pd.Series,
        alphas: pd.Series,
        sizes: pd.Series,
        **kwargs,
    ) -> None:
        """Draw nodes as a scatter trace on the Plotly figure."""
        x_vals = []
        y_vals = []
        marker_colors = []
        marker_sizes = []
        marker_opacities = []
        hover_texts = []
        node_labels = []

        hover_text = node_hover_text(nt)

        size_scale = kwargs.get("size_scale", 1.0)
        plotly_size_scale = kwargs.get("plotly_size_scale", 8)

        for node, row in nt.iterrows():
            px, py = pos[node]
            x_vals.append(px)
            y_vals.append(py)
            marker_colors.append(rgba_to_plotly_str(colors[node]))
            marker_opacities.append(float(alphas[node]))
            marker_sizes.append(float(sizes[node]) * size_scale * plotly_size_scale)
            hover_texts.append(hover_text[node])
            node_labels.append(str(node))

        axes.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode="markers",
                marker=dict(
                    color=marker_colors,
                    size=marker_sizes,
                    opacity=marker_opacities,
                    line=dict(width=0),
                ),
                text=hover_texts,
                hoverinfo="text",
                name="nodes",
                customdata=node_labels,
            )
        )

    def draw_edges(
        self,
        axes: go.Figure,
        et: pd.DataFrame,
        pos: Dict[Hashable, np.ndarray],
        path_coords: List,
        colors: pd.Series,
        alphas: pd.Series,
        lw: pd.Series,
        line_type: str,
        pos_cloned: Optional[Dict] = None,
        **kwargs,
    ) -> None:
        """Draw edges on the Plotly figure."""
        hover_text = edge_hover_text(et)
        aes_kw = kwargs.get("aes_kw", {})

        if line_type == "matrix":
            self.draw_matrix_edges(
                axes, et, path_coords, colors, alphas, lw, hover_text
            )
        else:
            self.draw_curve_edges(
                axes, et, path_coords, colors, alphas, lw, hover_text
            )

    def draw_curve_edges(
        self,
        axes: go.Figure,
        et: pd.DataFrame,
        path_coords: List,
        colors: pd.Series,
        alphas: pd.Series,
        lw: pd.Series,
        hover_text: pd.Series,
    ) -> None:
        """Draw curved/straight line edges as individual traces."""
        for i, (idx, row) in enumerate(et.iterrows()):
            if i >= len(path_coords):
                break

            coords = path_coords[i]
            if isinstance(coords, tuple):
                coords = np.array([list(coords)])

            if len(coords) >= 3:
                curve = bezier_curve(coords, n_points=30)
                x_vals = curve[:, 0].tolist()
                y_vals = curve[:, 1].tolist()
            else:
                x_vals = [coords[0][0], coords[1][0]]
                y_vals = [coords[0][1], coords[1][1]]

            x_vals.append(None)
            y_vals.append(None)

            color_str = rgba_to_plotly_str(colors[idx])
            alpha_val = float(alphas[idx])
            lw_val = float(lw[idx])

            axes.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode="lines",
                    line=dict(
                        color=color_str,
                        width=max(lw_val, 0.5),
                    ),
                    opacity=alpha_val,
                    text=hover_text[idx],
                    hoverinfo="text",
                    showlegend=False,
                    name="edges",
                )
            )

    def draw_matrix_edges(
        self,
        axes: go.Figure,
        et: pd.DataFrame,
        path_coords: List,
        colors: pd.Series,
        alphas: pd.Series,
        lw: pd.Series,
        hover_text: pd.Series,
    ) -> None:
        """Draw matrix plot edges as scatter markers."""
        x_vals = []
        y_vals = []
        marker_colors = []
        marker_sizes = []
        marker_opacities = []
        hover_texts = []

        for i, (idx, row) in enumerate(et.iterrows()):
            if i >= len(path_coords):
                break

            coord = path_coords[i]
            x, y = coord[0], coord[1]
            x_vals.append(x)
            y_vals.append(y)
            marker_colors.append(rgba_to_plotly_str(colors[idx]))
            marker_opacities.append(float(alphas[idx]))
            marker_sizes.append(float(lw[idx]) * 5)
            hover_texts.append(hover_text[idx])

        axes.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode="markers",
                marker=dict(
                    color=marker_colors,
                    size=marker_sizes,
                    opacity=marker_opacities,
                ),
                text=hover_texts,
                hoverinfo="text",
                showlegend=False,
                name="edges",
            )
        )

    def despine(self, axes: go.Figure) -> None:
        """Remove axis lines, ticks, and grid."""
        axes.update_xaxes(
            showline=False, showticklabels=False, showgrid=False, zeroline=False
        )
        axes.update_yaxes(
            showline=False, showticklabels=False, showgrid=False, zeroline=False
        )

    def set_aspect_equal(self, axes: go.Figure) -> None:
        """Set equal aspect ratio on the Plotly figure."""
        axes.update_yaxes(scaleanchor="x", scaleratio=1)

    def rescale(self, axes: go.Figure, pos_data, plot_type: str = "default") -> None:
        """Set axis ranges to fit the data."""
        if isinstance(pos_data, dict) and len(pos_data) > 0:
            all_pos = np.array(list(pos_data.values()))
            x_vals = all_pos[:, 0]
            y_vals = all_pos[:, 1]

            xmin, xmax = x_vals.min(), x_vals.max()
            ymin, ymax = y_vals.min(), y_vals.max()

            padding_x = max((xmax - xmin) * 0.1, 1)
            padding_y = max((ymax - ymin) * 0.1, 1)

            axes.update_xaxes(range=[xmin - padding_x, xmax + padding_x])
            axes.update_yaxes(range=[ymin - padding_y, ymax + padding_y])

    def get_figure(self, axes: go.Figure) -> go.Figure:
        """Return the Plotly Figure object."""
        return axes
