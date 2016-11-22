Watch Elasticsearch CLI
=======================

A CLI tool that can be used to watch Elasticsearch cluster.
*This work is under development.*

Synopsis
--------

The tool supports the following options:

- `help` - lists the options below with their usage and default values
- `duration` - tool will run for this many seconds/minutes/hours/forever
- `interval` - tool will poll ES and print stats every this many seconds
- `url` - ES url e.g. https://logging-es:9200
- `username`
- `password`
- `client_cert`
- `client_key`
- `ca_cert`
- `format` - text or json
   - could use _cat endpoints for text and regular endpoints for json
- `category` - for example, from https://www.elastic.co/guide/en/elasticsearch/guide/current/_cat_api.html
   - there are endpoints for allocation, shards, master, nodes, indices, etc.

Usage
-----

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

    $ pip install -e .[test]

If you'd like to run all tests for this project (*assuming you've written
some*), you would run the following command::

    $ python setup.py test

This will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.

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

Built on top of `skele-cli <https://github.com/rdegges/skele-cli.git>`_ skeleton.


License
-------

Watches CLI is licensed under the `Apache License, Version 2.0 <http://www.apache.org/licenses/>`_.
