Watch Elasticsearch CLI
=======================

CLI tool to pull statistics from Elasticsearch.

Build status
------------

.. image:: https://secure.travis-ci.org/ViaQ/watches-cli.png
   :target: http://travis-ci.org/#!/ViaQ/watches-cli

Support Matrix
--------------

The following combinations are regularly tested.

=======  =============  ========
watches  Elasticsearch  Python
=======  =============  ========
1.0.3    2.4.4          2.7, 3.5
-------  -------------  --------
1.0.2    2.4.4          2.7, 3.5
-------  -------------  --------
1.0.1    2.4.4          2.7
=======  =============  ========


Synopsis
--------

The tool uses `docopt <http://docopt.org/>`_ to describe command line language and supports the following options::

    Usage:
      watches cluster_health     [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--transform=TYPE] [--local --index=INDEX --level=LEVEL]
      watches cluster_state      [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--transform=TYPE] [--local --index=INDEX --metric=METRIC]
      watches cluster_stats      [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--transform=TYPE]
      watches nodes_stats        [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--transform=TYPE] [--metric=METRIC]
      watches nodes_info         [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--transform=TYPE] [--node_id=NODE_ID --metric=METRIC]
      watches indices_stats      [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--transform=TYPE] [--level=LEVEL --index=INDEX]
      watches nodes_hotthreads   [-i=INTERVAL -d=DURATION --url=URL -bsv] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--node_id=NODE_ID --threads=THREADS --delay=DELAY --type=TYPE]
      watches just_nodes_stats   [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--metric=METRIC]
      watches just_indices_stats [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--level=LEVEL --index=INDEX]
      watches -h
      watches --version

    Options:
      -d=DURATION, --duration=DURATION   How long the watches should run in seconds. Use value '-1' to run forever. [default: 0].
      -i=INTERVAL, --interval=INTERVAL   Interval between data retrievals. Apply if 'duration' > 0. [default: 3].
      --url=URL           URL of ES node HTTP endpoint [default: http://localhost:9200].
      -b                  Disable python output buffering (not recommended for production use).
      -l                  Single line output (no pretty-print JSON formatting).
      -t, --timestamp     Add timestamp field to data. The value is local datetime converted to UTC in ISO 8601 format.
      -s, --sniff         Turn on sniffing.
      -v, --verbose       Print more debug info: input options, ... etc.
      -f=FILTER, --filter_path=FILTER   Filter returned JSON (see http://elasticsearch-py.readthedocs.io/en/master/api.html#response-filtering)
      --username=USERNAME Username to authenticate with
      --password=PASSWORD Password to authenticate with
      --cacert=CACERT     Path to Certification Authority Certificate pem file
      --cert=CERT         Path to Client Certificate pem file
      --key=KEY           Path to Client Key pem file
      --level=LEVEL       Aggregation level of returned data, valid options: node/cluster, indices and shards [default: cluster].
      --local             Return the local node information instead of master node [default: false].
      --node_id=NODE_ID   A comma-separated list of node IDs or names to limit the returned information; use `_local` to return information from local node you're connecting to [default: ].
      --index=INDEX       A comma-separated list of index names; use `_all` or empty string to perform the operation on all indices.
      --metric=METRIC     A comma-separated list of metric names; use `_all` or empty string to perform the operation for all metrics.
      --threads=THREADS   Specify the number of threads to provide information for.
      --delay=DELAY       Delay (interval) to do the second sampling of threads.
      --type=TYPE         The type of threads to sample (default: cpu), valid choices are: 'cpu', 'wait', 'block'.
      --transform=TYPE    Transform JSON response (see online doc for more details). Valid choices: 'nested'.
      -h, --help          Show this screen.
      --version           Show version.
      --header=HEADER     Custom HTTP header to add to the request (e.g. --header="X-Proxy-Remote-User: username")

    Examples:
      # Get cluster health from specified HTTP endpoint with added "timestamp" field in the response
      $ watches cluster_health --timestamp --url=http://127.0.0.1:9200

      # Get cluster health every 1 second, run forever until process is terminated
      $ watches cluster_health --interval=1 --duration=-1

      # Get cluster health every 1 second during next 10 seconds and use sniffing
      $ watches cluster_health --interval=1 --duration=10 --sniff

      # Alternatively, using short option notation
      $ watches cluster_health -i 1 -d 10 -s

      # Get cluster health from secured node
      $ watches cluster_health \
          --url=https://localhots:9200 \
          --cacert /tmp/search-guard-ssl/example-pki-scripts/ca/chain-ca.pem \
          --cert /tmp/search-guard-ssl/example-pki-scripts/kirk.crt.pem \
          --key /tmp/search-guard-ssl/example-pki-scripts/kirk.key.pem

      # Filter cluster health for status fields
      $ watches cluster_health --level=shards -f status -f indices.*.status -f indices.*.shards.*.status

      Notice:
        Option --filter_path works under original context for commands 'just_nodes_stats' and 'just_indices_stats'.
        For example, if command 'just_indices_stats' is called the 'indices_stats' command is executed first, then
        --filter_path option is applied and only then the result data is transformed into 'just_indices_stats' output.

To connect to Elasticsearch cluster ``watches`` uses official
`elasticsearch-py <https://github.com/elastic/elasticsearch-py/>`_ client which
can use `Sniffing <http://elasticsearch-py.readthedocs.io/en/master/index.html#sniffing>`_.
It is recommended to use ``--sniff`` option (see above) to enable sniffing for long running tasks.

Install
-------

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

    $ pip install -e .[test]

Test
----

If you'd like to run all tests for this project, you would run the following command::

    $ python setup.py test

This will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.

Read `Testing.md <./tests/Testing.md>`_ to learn more details.

Release
-------

If you'd like to cut a new release of this CLI tool, and publish it to
the Python Package Index (`PyPI <https://pypi.python.org/pypi>`_), you can do so
by following the following `tutorial <http://peterdowns.com/posts/first-time-with-pypi.html>`_
or by running::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*

This will build both a source tarball of your CLI tool, as well as a newer wheel
build (*and this will, by default, run on all platforms*).

The ``twine upload`` command (which requires you to install the `twine
<https://pypi.python.org/pypi/twine>`_ tool) will then securely upload your
new package to PyPI so everyone in the world can use it!

Do not forget to update version by modifying `__init__.py <watches/__init__.py>`_
and `setup.py <setup.py>`_ files (download URL and other if applicable).

Credits
-------

Built on top of `skele-cli <https://github.com/rdegges/skele-cli.git>`_ skeleton, read
`skele-cli blog post <https://stormpath.com/blog/building-simple-cli-interfaces-in-python>`_
to learn more.


License
-------

Watches CLI is licensed under the `Apache License, Version 2.0 <http://www.apache.org/licenses/>`_.
