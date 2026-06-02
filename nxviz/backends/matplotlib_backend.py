"""Matplotlib backend for nxviz.

Wraps the existing matplotlib rendering code as a PlotBackend implementation.
"""

from typing import Any, Dict, Hashable, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Circle

from nxviz import lines


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
