"""The Nodes Info command."""


from .base import Base


class NodesInfo(Base):
    """Get nodes info"""

    def getData(self):
        return self.es.nodes.info(node_id=self.options['--node_id'])