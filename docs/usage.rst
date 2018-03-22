=====
Usage
=====


.. toctree::
   :maxdepth: 4


To use nxviz in a project::

    from nxviz.plots import CircosPlot

    # Assume we have a professional network of physicians belonging
    # to hospitals.
    c = CircosPlot(G,
                   node_color='affiliation',
                   node_grouping='affiliation')
    c.draw()

    plt.show()  # only needed in scripts
