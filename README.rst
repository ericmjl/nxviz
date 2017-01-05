===============================
nxviz
===============================

.. image:: https://badges.gitter.im/ericmjl/nxviz.svg
   :alt: Join the chat at https://gitter.im/ericmjl/nxviz
   :target: https://gitter.im/ericmjl/nxviz?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


.. image:: https://img.shields.io/pypi/v/nxviz.svg
        :target: https://pypi.python.org/pypi/nxviz

.. image:: https://img.shields.io/travis/ericmjl/nxviz.svg
        :target: https://travis-ci.org/ericmjl/nxviz

.. image:: https://readthedocs.org/projects/nxviz/badge/?version=latest
        :target: https://nxviz.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/ericmjl/nxviz/shield.svg
     :target: https://pyup.io/repos/github/ericmjl/nxviz/
     :alt: Updates


`nxviz` is a graph visualization package for NetworkX. With nxviz, you can create beautiful graph visualizations by a **declarative** API. Here's an example.

.. code:: python

    # Assume we have a professional network of physicians belonging to hospitals.
    c = CircosPlot(G, node_color='affiliation', node_grouping='affiliation')
    c.draw()
    plt.show()  # only needed in scripts


Check out the examples for more details!

* Free software: MIT license
* Documentation: https://nxviz.readthedocs.io.


Features
--------

* Declarative API.
* Works with NetworkX, one of the more popular graph libraries in Python.

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
