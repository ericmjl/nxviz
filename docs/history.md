# Release History

## 0.8.0 (2026-06-02)

* Added multi-backend support with `PlotBackend` protocol and `get_backend()` factory.
* Added Plotly interactive backend (`backend="plotly"`) for all six plot types.
* Added `nxviz/paths.py` for backend-agnostic edge path coordinate computation.
* Optional plotly dependency via `pip install nxviz[plotly]`.

## 0.7.6 (2025-03-01)

* Added `__all__` attribute to `__init__.py` for explicit module exports.
* Refined test parameters for polar-cartesian conversion.
* Switched build system from `setuptools` to `hatchling`.
* Removed legacy config files (`.editorconfig`, `.pyup.yml`, `.readthedocs.yml`, `Makefile`).

## 0.7.0 (2021-XX-XX)

* Major refactor behind-the-scenes with a functional API.

## 0.6.3 (2020-XX-XX)

* Version bump release.

## 0.4.0 (2018-06-19)

* Added `nxviz.io` module.

## 0.3.7 (2018-XX-XX)

* Node labels in CircosPlot can now be rotated with the `rotate_labels`
  argument.

## 0.3.6 (2018-02-20)

* Implemented edge colours, thanks to @noragak.

## 0.3.5 (2018-01-20)

* Disabled health checks on certain tests.
* Added ability to configure plot size.
* Added docs on preparing a new release.
* Updated dependencies.

## 0.3.2 (2017-09-18)

* All plots except for HivePlot are implemented.
* Implemented auto-colorbar for plots that have continuous node colors.

## 0.1.0 (2016-07-15)

* First release on PyPI.
