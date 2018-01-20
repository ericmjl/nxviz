Release Protocol
================

1. Run `bumpversion`.
    1. Patch: `bumpversion patch` (e.g. 0.3.4 -> 0.3.5)
    1. Minor version: `bumpversion minor` (e.g. 0.3.4 -> 0.4.0)
    1. Major version: `bumpversion major` (e.g. 0.3.4 -> 1.0)
1. Upload to `PyPI`.
    1. `rm dist/*`
    1. `python setup.py bdist_wheel sdist`
    1. `twine upload dist/*`
    1. `rm dist/*`
1. Update conda-forge recipe.
    1. Checkout new branch in conda-forge recipe, named `nxviz-{version}`. (Substitue in correct version.)
    1. Update the `meta.yaml` recipe.
    1. Push to `ericmjl/nxviz-feedstock`.
    1. PR into `conda-forge/nxviz-feedstock`.
