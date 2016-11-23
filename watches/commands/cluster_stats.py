"""The Cluster Stats command."""


from .base import Base


class ClusterStats(Base):
    """Get cluster stats"""

    def getData(self):
        return self.es.cluster.stats()

