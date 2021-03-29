"""Tests for utilities."""

import pytest

import os

import matplotlib.pyplot as plt

from matplotlib.testing.compare import compare_images

from nxviz.utils import (
    infer_data_type,
    is_data_diverging,
    is_data_homogenous,
    is_groupable,
    num_discrete_groups,
)

categorical = ["sun", "moon", "light"]
ordinal = [1, 2, 3, 4, 5]
mixed = ["sun", 1, 2.5]
continuous = [1.0, 1.1, 1.2]
diverging_ordinal = [1, 2, 3, 4, -1, -2, -3, -4]
diverging_continuous = [0.0, 0.1, 0.2, 0.3, -0.1, -0.2, -0.3]
unknown_type = [(1, 2), (2, 3), (3, 4)]
binomial = ["hello", "interesting"]
binomial_integer = [0, 1]
binomial_float = [0.1, 0.2]


def test_is_data_homogenous():
    """Test for is_data_homogeneous."""
    assert not is_data_homogenous(mixed)
    assert is_data_homogenous(categorical)
    assert is_data_homogenous(ordinal)
    assert is_data_homogenous(continuous)


def test_infer_data_type():
    """Test for infer_data_type."""
    assert infer_data_type(categorical) == "categorical"
    assert infer_data_type(ordinal) == "ordinal"
    assert infer_data_type(continuous) == "continuous"


def test_is_data_diverging():
    """Test for is_data_diverging."""
    assert is_data_diverging(diverging_ordinal)
    assert is_data_diverging(diverging_continuous)

    assert not is_data_diverging(ordinal)
    assert not is_data_diverging(continuous)


def test_unknown_data_type():
    """Test that an unknown data type raises a value error."""
    with pytest.raises(ValueError):
        infer_data_type(unknown_type)


def test_is_groupable():
    """Test for is_groupable."""
    assert is_groupable(categorical)
    with pytest.raises(AssertionError):
        is_groupable(mixed)


def test_num_discrete_groups():
    """Test that num_discrete_groups works correctly."""
    assert num_discrete_groups(categorical) == 3
    assert num_discrete_groups(ordinal) == 5


def test_binomial():
    """Test for is_data_type for binomial data."""
    assert infer_data_type(binomial) == "categorical"
    assert infer_data_type(binomial_float) == "categorical"
    assert infer_data_type(binomial_integer) == "categorical"


def diff_plots(plot, plot_fn, baseline_dir, result_dir):
    """Utility function to diff two plots."""
    plot.draw()
    img_fn = plot_fn
    baseline_img_path = os.path.join(baseline_dir, img_fn)
    result_img_path = os.path.join(result_dir, img_fn)
    plt.savefig(result_img_path)
    diff = compare_images(baseline_img_path, result_img_path, tol=0)
    return diff
