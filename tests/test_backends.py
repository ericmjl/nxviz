"""Tests for nxviz.backend module — PlotBackend protocol and factory."""

import pytest

from nxviz.backend import BACKEND_REGISTRY, get_backend


class TestGetBackend:
    def test_matplotlib_returns_backend(self):
        backend = get_backend("matplotlib")
        assert backend is not None

    def test_matplotlib_has_required_methods(self):
        backend = get_backend("matplotlib")
        assert hasattr(backend, "create_axes")
        assert hasattr(backend, "draw_nodes")
        assert hasattr(backend, "draw_edges")
        assert hasattr(backend, "despine")
        assert hasattr(backend, "set_aspect_equal")
        assert hasattr(backend, "rescale")
        assert hasattr(backend, "get_figure")

    def test_plotly_returns_backend(self):
        backend = get_backend("plotly")
        assert backend is not None

    def test_plotly_has_required_methods(self):
        backend = get_backend("plotly")
        assert hasattr(backend, "create_axes")
        assert hasattr(backend, "draw_nodes")
        assert hasattr(backend, "draw_edges")
        assert hasattr(backend, "despine")
        assert hasattr(backend, "set_aspect_equal")
        assert hasattr(backend, "rescale")
        assert hasattr(backend, "get_figure")

    def test_unknown_backend_raises_valueerror(self):
        with pytest.raises(ValueError, match="Unknown backend"):
            get_backend("nonexistent")

    def test_unknown_backend_lists_available(self):
        with pytest.raises(ValueError, match="matplotlib") as exc_info:
            get_backend("nonexistent")
        assert "plotly" in str(exc_info.value)


class TestRegistry:
    def test_registry_has_matplotlib(self):
        assert "matplotlib" in BACKEND_REGISTRY

    def test_registry_has_plotly(self):
        assert "plotly" in BACKEND_REGISTRY

    def test_matplotlib_is_default(self):
        backend = get_backend()
        assert type(backend).__name__ == "MatplotlibBackend"
