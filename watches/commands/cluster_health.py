"""The Cluster Health command."""


from .base import Base


class ClusterHealth(Base):
    """Get cluster health"""

    def getData(self):
        return self.es.cluster.health(wait_for_status='yellow', request_timeout=1)

