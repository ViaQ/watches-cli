"""The Cluster State command."""


from .base import Base


class ClusterState(Base):
    """Get cluster state"""

    def getData(self):
        return self.es.cluster.state()

