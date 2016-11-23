"""The Cluster Health command."""


from .base import Base


class ClusterHealth(Base):
    """Get cluster health"""

    def getData(self):
        return self.es.cluster.health(level=self.options['--level'], local=self.options['--local'], request_timeout=1)

