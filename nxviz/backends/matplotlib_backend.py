"""Matplotlib backend for nxviz.

Wraps the existing matplotlib rendering code as a PlotBackend implementation.
"""

from typing import Any, Dict, Hashable, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Circle, Polygon

from nxviz import lines
from nxviz.polcart import to_cartesian


class MatplotlibBackend:
    """Matplotlib-based rendering backend.

    This is the default backend that preserves the exact same rendering
    behavior as the pre-backend nxviz implementation.
    """

    def create_axes(self) -> Any:
        """Return the current matplotlib axes."""
        return plt.gca()

    def draw_nodes(
        self,
        axes: Any,
        nt: pd.DataFrame,
        pos: Dict[Hashable, np.ndarray],
        colors: pd.Series,
        alphas: pd.Series,
        sizes: pd.Series,
        **kwargs,
    ) -> None:
        """Draw nodes as Circle patches on the matplotlib axes."""
        encodings_kwargs = kwargs.get("encodings_kwargs", {})
        for r, d in nt.iterrows():
            kw = {
                "fc": colors[r],
                "alpha": alphas[r],
                "radius": sizes[r],
                "zorder": 2,
            }
            kw.update(encodings_kwargs)
            c = Circle(xy=pos[r], **kw)
            axes.add_patch(c)

    def draw_edges(
        self,
        axes: Any,
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
        """Draw edges on the matplotlib axes.

        Uses nxviz.lines functions to create matplotlib patches,
        maintaining identical rendering to the original implementation.
        """
        aes_kw = kwargs.get("aes_kw", {"facecolor": "none"})

        if line_type == "circos":
            patches = lines.circos(et, pos, colors, alphas, lw, aes_kw)
        elif line_type == "line":
            patches = lines.line(et, pos, colors, alphas, lw, aes_kw)
        elif line_type == "arc":
            patches = lines.arc(et, pos, colors, alphas, lw, aes_kw)
        elif line_type == "hive":
            patches = lines.hive(et, pos, pos_cloned, colors, alphas, lw, aes_kw)
        elif line_type == "matrix":
            patches = lines.matrix(et, pos, pos_cloned, colors, alphas, lw, aes_kw)
        else:
            patches = lines.line(et, pos, colors, alphas, lw, aes_kw)

        for patch in patches:
            axes.add_patch(patch)

    def despine(self, axes: Any) -> None:
        """Remove spines and ticks from matplotlib axes."""
        for spine in axes.spines:
            axes.spines[spine].set_visible(False)
        axes.xaxis.set_visible(False)
        axes.yaxis.set_visible(False)

    def set_aspect_equal(self, axes: Any) -> None:
        """Set equal aspect ratio on matplotlib axes."""
        axes.set_aspect("equal")

    def rescale(self, axes: Any, pos_data, plot_type: str = "default") -> None:
        """Rescale matplotlib axes to fit data."""
        axes.relim()
        axes.autoscale_view()

        if plot_type == "arc":
            ymin, ymax = axes.get_ylim()
            n_nodes = len(pos_data) if isinstance(pos_data, dict) else 1
            maxheight = int(n_nodes) + 1
            axes.set_ylim(ymin - 1, maxheight)
            axes.set_xlim(-1, n_nodes * 2 + 1)
        elif plot_type in ("hive", "square"):
            xmin, xmax = axes.get_xlim()
            ymin, ymax = axes.get_ylim()
            newmax = max([xmax, ymax, -xmin, -ymin])
            axes.set_xlim(-newmax, newmax)
            axes.set_ylim(-newmax, newmax)

    def get_figure(self, axes: Any) -> Any:
        """Return the matplotlib axes object."""
        return axes

    def draw_arcs(
        self,
        axes: Any,
        group_arcs: pd.DataFrame,
        radius: float,
        **kwargs,
    ) -> None:
        """Draw arc segments for chord diagrams."""
        arc_half = 0.025 * radius

        for _, row in group_arcs.iterrows():
            n_pts = max(int((row["end_angle"] - row["start_angle"]) * 50), 10)
            thetas = np.linspace(row["start_angle"], row["end_angle"], n_pts)
            outer_x = (radius + arc_half) * np.cos(thetas)
            outer_y = (radius + arc_half) * np.sin(thetas)
            inner_x = (radius - arc_half) * np.cos(thetas[::-1])
            inner_y = (radius - arc_half) * np.sin(thetas[::-1])

            verts_x = np.concatenate([outer_x, inner_x])
            verts_y = np.concatenate([outer_y, inner_y])
            verts = np.column_stack([verts_x, verts_y])

            poly = Polygon(
                verts,
                closed=True,
                facecolor=row["color"],
                edgecolor=row["color"],
                linewidth=0.5,
                zorder=2,
            )
            axes.add_patch(poly)

    def draw_ribbons(
        self,
        axes: Any,
        ribbon_data: list,
        **kwargs,
    ) -> None:
        """Draw ribbons connecting arc segments for chord diagrams."""
        for ribbon in ribbon_data:
            coords = ribbon["path_coords"]
            if len(coords) < 3:
                continue

            poly = Polygon(
                coords,
                closed=True,
                facecolor=ribbon["color"],
                edgecolor=ribbon["color"],
                alpha=ribbon["alpha"],
                linewidth=0,
                zorder=1,
            )
            axes.add_patch(poly)

    def draw_arc_labels(
        self,
        axes: Any,
        group_arcs: pd.DataFrame,
        radius: float,
        **kwargs,
    ) -> None:
        """Draw group labels outside arc segments for chord diagrams."""
        arc_half = 0.025 * radius
        label_radius = radius + arc_half + radius * 0.08

        for _, row in group_arcs.iterrows():
            mid_angle = (row["start_angle"] + row["end_angle"]) / 2
            x, y = to_cartesian(label_radius, mid_angle)

            angle_deg = np.rad2deg(mid_angle)
            if 90 < angle_deg <= 270:
                rotation = angle_deg - 180
                ha = "right"
            else:
                rotation = angle_deg
                ha = "left"

            axes.text(
                x,
                y,
                str(row["group"]),
                ha=ha,
                va="center",
                rotation=rotation,
                rotation_mode="anchor",
                fontsize=10,
                zorder=3,
            )
