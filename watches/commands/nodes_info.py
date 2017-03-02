"""The Nodes Info command."""


from .base import Base


class NodesInfo(Base):
    """Get nodes info"""

    def getData(self):
        args = {
            'node_id': self.options['--node_id'],
            'metric': self.options['--metric']
        }
        self.check_filter_path(args)
        return self.es.nodes.info(**args)

    def transformNestedData(self, data):
        if 'nodes' in data:
            data['nodes'] = self.nestedNodes(data['nodes'])
        return data