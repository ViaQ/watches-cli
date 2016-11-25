"""The Indices Stats command."""


from .base import Base


class IndicesStats(Base):
    """Get indices stats"""

    def getData(self):
        return self.es.indices.stats(index=self.options['--index'], level=self.options['--level'])