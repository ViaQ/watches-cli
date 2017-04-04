"""The Indices Stats command."""


from .base import Base


class IndicesStats(Base):
    """Get indices stats"""

    def getData(self):
        args = {
            'index': self.options['--index'],
            'level': self.options['--level']
        }
        self.check_filter_path(args)
        return self.es.indices.stats(**args)

    def transformNestedData(self, data):
        # Hot fix, this should be solved more generally using field renaming (see #33)
        if '_all' in data:
            data['indices_summary'] = data['_all']
            del data['_all']

        if 'indices' in data:
            data['indices'] = self.nestedIndicesAndShards(data['indices'])

        return data

    def nestedShards(self, shards):
        return self.nestedShardsArray(shards)