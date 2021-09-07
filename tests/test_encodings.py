"""Tests for encodings submodule."""

from nxviz import encodings as aes
import pytest
import pandas as pd
from random import choice
import numpy as np


def categorical_series():
    """Generator for categorical series."""
    categories = "abc"
    return pd.Series([choice(categories) for _ in range(30)])


def continuous_series():
    """Generator for continuous-valued series."""
    values = np.linspace(0, 2, 100)
    return pd.Series(values)


def ordinal_series():
    """Generator for an ordinal series."""
    values = [1, 2, 3, 4]
    return pd.Series(values)


@pytest.fixture
def too_many_categories():
    """Generator for an categorical series with too many categories."""
    categories = list("abcdeefghijklmnop")
    return pd.Series(categories)


@pytest.mark.parametrize(
    "data, category",
    [
        (categorical_series(), "categorical"),
        (continuous_series(), "continuous"),
        (ordinal_series(), "ordinal"),
    ],
)
def test_data_cmap(data, category):
    """Test data_cmap."""
    cmap, data_family = aes.data_cmap(data)
    assert data_family == category


def test_data_cmap_errors(too_many_categories):
    """Test that data_cmap errors with too man categories."""
    with pytest.raises(ValueError):
        aes.data_cmap(too_many_categories)


@pytest.mark.parametrize(
    "data",
    [
        (categorical_series()),
        (continuous_series()),
        (ordinal_series()),
    ],
)
def test_data_color(data):
    """Test data_color."""
    colors = aes.data_color(data, data)
    assert isinstance(colors, pd.Series)


@pytest.mark.parametrize(
    "data",
    [
        (continuous_series()),
        (ordinal_series()),
    ],
)
def test_data_size(data):
    """Test data_size."""
    sizes = aes.data_size(data, data)
    assert isinstance(sizes, pd.Series)
    assert np.allclose(sizes, np.sqrt(data))


@pytest.mark.parametrize(
    "data",
    [
        (continuous_series()),
        (ordinal_series()),
    ],
)
def test_data_linewidth(data):
    """Test data_linewidth."""
    lw = aes.data_linewidth(data, data)
    assert isinstance(lw, pd.Series)
    assert np.allclose(lw, data)
