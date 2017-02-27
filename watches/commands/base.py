"""The base command."""


from datetime import datetime
from json import dumps
from watches.util import ESClientProducer


class Base(object):
    """A base command."""

    TEXT_PLAIN = 'plain/text'
    JSON_APPLICATION = 'application/json'

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

        if self.options["--verbose"]:
            print 'Supplied options:', dumps(self.options, indent=2, sort_keys=True)

        self.es = ESClientProducer.create_client(self.options)

    def run(self):
        # Not sure if this is the best way to convert localtime to UTC in ISO 8601 format
        ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        data = self.getData()

        # Treat JSON_APPLICATION response differently than TEXT_PLAIN
        if self.JSON_APPLICATION == self.getResponseContentType():

            if self.options["--timestamp"]:
                data['timestamp'] = ts

            if self.options["--transform"]:
                data = self.transformData(data)

            if self.options["-l"]:
                print dumps(data, default=lambda x:str(x))
            else:
                print dumps(data, indent=2, sort_keys=False, default=lambda x:str(x))
        else:
            print data

    def getData(self):
        raise NotImplementedError('Method getData() not implemented')

    def getResponseContentType(self):
        """Response MIME type. By default we assume JSON, make sure to override if needed."""
        return self.JSON_APPLICATION

    def transformData(self, data):
        """
        Data can be transformed before sending to client.
        Currently, the only transformation type implemented is 'nested'.
        :param data:
        :return:
        """
        transform = self.options['--transform']
        if transform:
            if transform == "nested":
                return self.transformNestedData(data)
            else:
                raise RuntimeError('Unsupported transform type')
        else:
            return data

    def transformNestedData(self, data):
        """
        If subclass supports 'nested' transformation then it needs to implement
        this method and it can use and override provided helper methods.
        By default the data is returned unchanged.

        :param data:
        :return:
        """
        return data

    def nestedNodes(self, nodes):
        """
        Helper method to transform nodes object.
        Subclass can override this if the default behaviour does not apply.

        :param nodes:
        :return:
        """
        if isinstance(nodes, dict):
            nodesArray = []
            for key in nodes:
                n = nodes[key]
                n['node'] = key
                nodesArray.append(n)
            return nodesArray
        return nodes

    def nestedNodesShardsArray(self, nodes):
        """
        Helper method to transform nodes shards array.
        Subclass can override this if the default behaviour does not apply.

        :param nodes:
        :return:
        """
        if isinstance(nodes, dict):
            shardsArray = []
            for node in nodes:
                if isinstance(nodes[node], list):
                    for shard in nodes[node]:
                        # shard['node'] = node
                        # node value ^^ is already there in the dict
                        shardsArray.append(shard)
                else:
                    raise RuntimeError('shards not in expected format')
        else:
            raise RuntimeError('shards not in expected format')
        return shardsArray

    def nestedIndices(self, indices):
        """
        Helper method to transform indices object.
        Subclass can override this if the default behaviour does not apply.

        :param indices:
        :return:
        """
        if isinstance(indices, dict):
            indicesArray = []
            for key in indices:
                i = indices[key]
                i['index'] = key
                indicesArray.append(i)
            return indicesArray
        else:
            return indices

    def nestedShards(self, shards):
        """
        Helper method to transform shards object.
        Subclass can override this if the default behaviour does not apply.

        :param shards:
        :return:
        """
        if isinstance(shards, dict):
            shardsArray = []
            for key in shards:
                s = shards[key]
                # convert shard id to number (this is how other admin REST APIs represent it)
                s['shard'] = int(key)
                shardsArray.append(s)
            return shardsArray
        else:
            return shards

    def nestedShardsArray(self, shards):
        """
        Helper method to transform shards array.
        This is useful in case REST API returns shards data in an array.

        :param shards:
        :return:
        """
        shardsArray = []
        if isinstance(shards, dict):
            for key in shards:
                if isinstance(shards[key], list):
                    for shard in shards[key]:
                        shard['shard'] = int(key)
                        shardsArray.append(shard)
                else:
                    raise RuntimeError('shards not in expected format')
        else:
            raise RuntimeError('shards not in expected format')
        return shardsArray

    def nestedIndicesAndShards(self, indices):
        """
        Helper method to transform indices and shards.
        This method is designed for cases where index contains 'shards' key as the top level field.

        :param indices:
        :return:
        """
        indices = self.nestedIndices(indices)
        for index in indices:
            if isinstance(index, dict):
                if 'shards' in index:
                    index['shards'] = self.nestedShards(index['shards'])
        return indices

    def check_filter_path(self, args):
        if self.options['--filter_path'] and self.options["--filter_path"] is not None and len(self.options["--filter_path"]) > 0:
            args.update({
                'filter_path': self.options['--filter_path']
            })
