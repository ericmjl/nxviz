"""Backend abstraction for nxviz rendering.

Defines the PlotBackend protocol and a factory function get_backend().
"""

from typing import Any, Dict, Hashable, List, Optional, Protocol, Tuple, Union

import numpy as np
import pandas as pd

BACKEND_REGISTRY: Dict[str, str] = {
    "matplotlib": "nxviz.backends.matplotlib_backend.MatplotlibBackend",
    "plotly": "nxviz.backends.plotly_backend.PlotlyBackend",
}


class PlotBackend(Protocol):
    """Protocol defining the rendering interface for nxviz backends."""

    def create_axes(self) -> Any:
        """Create and return a backend-specific axes/figure object."""
        ...

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
        """Render all nodes onto the axes."""
        ...

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
        """Render all edges onto the axes."""
        ...

    def despine(self, axes: Any) -> None:
        """Remove axis spines and tick marks."""
        ...

    def set_aspect_equal(self, axes: Any) -> None:
        """Set equal aspect ratio on the axes."""
        ...

    def rescale(self, axes: Any, pos_data, plot_type: str = "default") -> None:
        """Adjust axis limits to fit the plotted data."""
        ...

    def get_figure(self, axes: Any) -> Any:
        """Return the top-level figure object for display/saving."""
        ...


def get_backend(name: str = "matplotlib") -> Any:
    """Return a backend instance by name.

    Parameters
    ----------
    name : str
        Backend name. One of: 'matplotlib', 'plotly'.

    Returns
    -------
    PlotBackend
        An instance of the requested backend.

    Raises
    ------
    ValueError
        If the backend name is not recognized.
    ImportError
        If the backend's required package is not installed.
    """
    if name not in BACKEND_REGISTRY:
        available = ", ".join(sorted(BACKEND_REGISTRY.keys()))
        raise ValueError(
            f"Unknown backend '{name}'. Available backends: {available}"
        )

    module_path, class_name = BACKEND_REGISTRY[name].rsplit(".", 1)
    try:
        import importlib

        module = importlib.import_module(module_path)
    except ImportError as e:
        if name == "plotly":
            raise ImportError(
                f"The '{name}' backend requires plotly. "
                "Install it with: pip install nxviz[plotly]"
            ) from e
        raise

    cls = getattr(module, class_name)
    return cls()
