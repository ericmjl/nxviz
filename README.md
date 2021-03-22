# nxviz

`nxviz` is a graph visualization package for NetworkX. With nxviz, you can create beautiful graph visualizations by a **declarative** API. Here's an example.


```python
# Assume we have a professional network of physicians belonging to hospitals.
c = CircosPlot(G, node_color='affiliation', node_grouping='affiliation')
c.draw()
plt.show()  # only needed in scripts
```

This is free software distributed under the MIT License.

## Installation

We recommend using [conda].

```
$ conda install -c conda-forge nxviz
```

Alternatively, it is also available on [PyPI].

```
$ pip install nxviz
```

[conda]: https://www.anaconda.com/download/
[PyPI]: https://pypi.python.org/pypi/nxviz

## Requirements

For requirements, consult the `requirements.txt` file in the GitHub repository. As a matter of practice, nxviz development will try (where relevant) to take advantage of the latest Python features. As of 18 September 2017, this means Python 3.6 is the "officially" supported version, as there are places where we use f-string formatting to simplify logging and debugging.

## Features

- Declarative API.
- Works with NetworkX, one of the more popular graph libraries in Python.
- Can build NetworkX graphs from a pandas DataFrame

## Feature Requests

If you have a feature request, please post it as an issue on the GitHub repository [issue tracker][issue]. Even better, put in a [PR] for it! I am more than happy to guide you through the codebase so that you can put in a contribution to the codebase - and I'll give you a digital `nxviz` contributor badge that you can put on your personal website, as a way of saying thanks!

Because nxviz is currently maintained by volunteers and has no fiscal support, any feature requests will be prioritized according to what maintainers encounter as a need in our day-to-day jobs. Please temper expectations accordingly.


[issue]: https://github.com/ericmjl/nxviz/issues
[PR]: https://github.com/ericmjl/nxviz/pulls

## Related Projects

- [Grandalf](https://github.com/bdcht/grandalf)

## Credits

This package was created with [Cookiecutter] and the [`audreyr/cookiecutter-pypackage`][pypkg] project template.

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[pypkg]: https://github.com/audreyr/cookiecutter-pypackage
