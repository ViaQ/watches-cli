"""
The Just Nodes Stats command.
To learn what the "Just" means in this context see #36
(https://github.com/ViaQ/watches-cli/issues/36)
"""


from .nodes_stats import NodesStats


class JustNodesStats(NodesStats):
    """Get "just" nodes stats"""

    def getData(self):
        # This command makes sense only for nested data format hence force nested transformation
        self.options[self.TRANSFORM_PARAM] = self.TRANSFORM_VALUE_NESTED
        return NodesStats.getData(self)

    def printData(self, data):
        if 'nodes' in data:
            for node in data['nodes']:
                # If timestamp key/value found in the root then copy it into all nested nodes
                if self.TIMESTAMP_KEY in data:
                    node[self.TIMESTAMP_KEY] = data[self.TIMESTAMP_KEY]

                NodesStats.printData(self, node)
