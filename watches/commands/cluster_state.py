"""The Cluster Health command."""


from json import dumps

from .base import Base


class ClusterState(Base):
    """Get cluster state"""

    def run(self):
        print 'cluster_state:', dumps(self.es.cluster.state(), indent=2, sort_keys=False)

