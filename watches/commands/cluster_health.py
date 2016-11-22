"""The Cluster Health command."""


from json import dumps

from .base import Base


class ClusterHealth(Base):
    """Get cluster health"""

    def run(self):
        print 'cluster_health:', dumps(self.es.cluster.health(wait_for_status='yellow', request_timeout=1), indent=2, sort_keys=False)

