Watch Elasticsearch CLI
=======================

A CLI tool that can be used to watch Elasticsearch cluster.
*This work is under development.*

Build status
------------

.. image:: https://secure.travis-ci.org/ViaQ/watches-cli.png
   :target: http://travis-ci.org/#!/ViaQ/watches-cli

Synopsis
--------

The tool uses `docopt <http://docopt.org/>`_ to describe command line language and supports the following options::

    Usage:
      watches cluster_health [--url=URL] [--timestamp] [--verbose] [--level=LEVEL] [--local]
      watches cluster_state  [--url=URL] [--timestamp] [--verbose]
      watches cluster_stats  [--url=URL] [--timestamp] [--verbose]
      watches nodes_stats    [--url=URL] [--timestamp] [--verbose]
      watches nodes_info     [--url=URL] [--timestamp] [--verbose] [--node_id=NODE_ID]
      watches -h | --help
      watches --version

    Options:
      -h --help             Show this screen.
      --version             Show version.
      --url=URL             URL of ES node HTTP endpoint [default: http://localhost:9200].
      --timestamp           Add timestamp field to data. The value is local datetime converted to UTC in ISO 8601 format.
      --verbose             Print more debug info: input options, ... etc.
      --level=LEVEL         LEVEL can be: cluster, indices or shards. [default: cluster].
      --local               Return the local node information instead of master node.
      --node_id=NODE_ID     A comma-separated list of node IDs or names to limit the returned information; use `_local` to return information from local node you're connecting to [default: ].

    Examples:
      watches cluster_health --timestamp --url=http://127.0.0.1:9200

Install, Test and Release
-------------------------

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

    $ pip install -e .[test]

If you'd like to run all tests for this project (*assuming you've written
some*), you would run the following command::

    $ python setup.py test

This will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.

Tests assume ES node running on ``http://localhost:9200``.

Lastly, if you'd like to cut a new release of this CLI tool, and publish it to
the Python Package Index (`PyPI <https://pypi.python.org/pypi>`_), you can do so
by running::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*

This will build both a source tarball of your CLI tool, as well as a newer wheel
build (*and this will, by default, run on all platforms*).

The ``twine upload`` command (which requires you to install the `twine
<https://pypi.python.org/pypi/twine>`_ tool) will then securely upload your
new package to PyPI so everyone in the world can use it!

Credits
-------

Built on top of `skele-cli <https://github.com/rdegges/skele-cli.git>`_ skeleton, read
`skele-cli blog post <https://stormpath.com/blog/building-simple-cli-interfaces-in-python>`_
to learn more.


License
-------

Watches CLI is licensed under the `Apache License, Version 2.0 <http://www.apache.org/licenses/>`_.