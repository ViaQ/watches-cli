"""The Cluster State command."""


from .base import Base


class ClusterState(Base):
    """Get cluster state"""

    def getData(self):
        args = {
            'local': self.options['--local'],
            'index': self.options['--index'],
            'metric': self.options['--metric']
        }
        self.check_filter_path(args)
        return self.es.cluster.state(**args)

    def transformNestedData(self, data):

        # for now skipping 'blocks' field

        if 'metadata' in data:
            metadata = data['metadata']
            if 'indices' in metadata:
                metadata['indices'] = self.nestedIndices(metadata['indices'])

        if 'nodes' in data:
            data['nodes'] = self.nestedNodes(data['nodes'])

        # routing_table.indices
        if 'routing_table' in data:
            if 'indices' in data['routing_table']:
                data['routing_table']['indices'] = self.nestedIndicesAndShards(data['routing_table']['indices'])

        # routing_nodes.nodes
        if 'routing_nodes' in data:
            if 'nodes' in data['routing_nodes']:
                data['routing_nodes']['nodes'] = self.nestedNodesShardsArray(data['routing_nodes']['nodes'])

        return data

    def nestedShards(self, shards):
        return self.nestedShardsArray(shards)

