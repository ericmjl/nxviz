"""Tests for polcart submodule."""
import numpy as np

from hypothesis import assume, given, settings
from hypothesis.strategies import floats
from nxviz.polcart import (
    to_cartesian,
    to_degrees,
    to_polar,
    to_proper_degrees,
    to_proper_radians,
    to_radians,
)


# @given(
#     floats(min_value=-1e3, max_value=1e3, allow_infinity=False, allow_nan=False),
#     floats(min_value=-1e3, max_value=1e3, allow_infinity=False, allow_nan=False),
# )
# def test_convert_xy(x, y):
#     """Test for conversion of cartesian to polar."""
#     assume(x != 0 and y != 0)
#     assume(abs(x) > 0.01 and abs(y) > 0.01)

#     # Test radians
#     r, theta = to_polar(x, y)
#     x_new, y_new = to_cartesian(r, theta)
#     assert np.allclose(x, x_new)
#     assert np.allclose(y, y_new)

#     # Test degrees
#     r, theta = to_polar(x, y, theta_units="degrees")
#     x_new, y_new = to_cartesian(r, theta, theta_units="degrees")
#     assert np.allclose(x, x_new)
#     assert np.allclose(y, y_new)


@given(
    floats(min_value=-1e6, max_value=1e6, allow_infinity=False, allow_nan=False),
    floats(
        min_value=0,
        max_value=2 * np.pi,
        allow_infinity=False,
        allow_nan=False,
    ),
)
def test_convert_rt(r, theta):
    """Test for conversion of polar to cartesian coordinates."""
    assume(r > 0.01 and r < 1e6)
    assume(np.isfinite(r) and np.isfinite(theta))

    x, y = to_cartesian(r, theta)
    r_new, theta_new = to_polar(x, y)

    assert np.allclose(r, r_new)
    assert np.allclose(abs(theta_new), abs(theta))


@given(floats())
def test_to_proper_radians(theta):
    """Test for to_proper_radians."""
    assume(np.isfinite(theta))
    theta = to_proper_radians(theta)
    assert theta <= np.pi and theta >= -np.pi


@given(floats())
def test_to_proper_degrees(theta):
    """Test for to_proper_degrees."""
    assume(np.isfinite(theta))
    theta = to_proper_degrees(theta)
    assert theta <= 180 and theta >= -180


@given(floats())
def test_to_degrees(theta):
    """Test for to_degrees."""
    assume(np.isfinite(theta))
    theta = to_degrees(theta)
    assert theta <= 180 and theta >= -180


@given(floats())
def test_to_radians(theta):
    """Test for to_radians."""
    assume(np.isfinite(theta))
    theta = to_radians(theta)
    assert theta <= np.pi and theta >= -np.pi
