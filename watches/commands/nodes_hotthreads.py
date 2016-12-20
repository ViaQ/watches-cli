"""The Nodes Hot Threads command."""


from .base import Base

class NodesHotThreads(Base):
    """Get nodes hot threads"""

    def getResponseContentType(self):
        return self.TEXT_PLAIN

    def getData(self):
        args = {
            'node_id': self.options['--node_id'],
            'threads': self.options['--threads'],
            'interval': self.options['--delay'],
            'doc_type': self.options['--type']
        }
        return self.es.nodes.hot_threads(**args)