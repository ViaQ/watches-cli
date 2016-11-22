"""The base command."""


from json import dumps

from elasticsearch import Elasticsearch


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        print 'You supplied the following options:', dumps(self.options, indent=2, sort_keys=True)
        self.es = Elasticsearch([options["--url"]])

    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')
