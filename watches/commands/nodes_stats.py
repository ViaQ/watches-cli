"""The Nodes Stats command."""


from .base import Base


class NodesStats(Base):
    """Get nodes stats"""

    def getData(self):
        return self.es.nodes.stats()