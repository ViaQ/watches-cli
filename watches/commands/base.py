"""The base command."""


from datetime import datetime
from json import dumps
from elasticsearch import Elasticsearch


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

        if self.options["--verbose"]:
            print 'Supplied options:', dumps(self.options, indent=2, sort_keys=True)

        if self.options["--sniff"]:
            self.es = Elasticsearch([options["--url"]],
                # sniff before doing anything
                sniff_on_start=True,
                # refresh nodes after a node fails to respond
                sniff_on_connection_fail=True,
                # and also every 60 seconds
                sniffer_timeout=60 )
        else:
            self.es = Elasticsearch([options["--url"]])

    def run(self):
        # Not sure if this is the best way to convert localtime to UTC in ISO 8601 format
        ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        data = self.getData()
        if self.options["--timestamp"]:
            data['timestamp'] = ts

        print dumps(data, indent=2, sort_keys=False, default=lambda x:str(x))

    def getData(self):
        raise NotImplementedError('You must implement the run() method yourself!')
