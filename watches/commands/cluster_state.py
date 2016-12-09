"""The Cluster State command."""


from .base import Base


class ClusterState(Base):
    """Get cluster state"""

    def getData(self):
        args = {
            'local': self.options['--local'],
            'index': self.options['--index'],
            'metric': self.options['--metric']
        }
        self.check_filter_path(args)
        return self.es.cluster.state(**args)

