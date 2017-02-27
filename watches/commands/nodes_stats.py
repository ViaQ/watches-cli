"""The Nodes Stats command."""


from .base import Base


class NodesStats(Base):
    """Get nodes stats"""

    def getData(self):
        args = {
            'metric': self.options['--metric']
        }
        self.check_filter_path(args)
        return self.es.nodes.stats(**args)

    def transformNestedData(self, data):
        if 'nodes' in data:
            data['nodes'] = self.nestedNodes(data['nodes'])
        return data