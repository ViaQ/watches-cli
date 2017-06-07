"""
The Just Indices Stats command.
To learn what the "Just" means in this context see #36
(https://github.com/ViaQ/watches-cli/issues/36)
"""


from .indices_stats import IndicesStats


class JustIndicesStats(IndicesStats):
    """Get "just" indices stats"""

    def getData(self):
        # This command makes sense only for nested data format hence force nested transformation
        self.options[self.TRANSFORM_PARAM] = self.TRANSFORM_VALUE_NESTED
        return IndicesStats.getData(self)

    def printData(self, data):
        if 'indices' in data:
            for index in data['indices']:
                # If timestamp key/value found in the root then copy it into all nested indices
                if self.TIMESTAMP_KEY in data:
                    index[self.TIMESTAMP_KEY] = data[self.TIMESTAMP_KEY]

                IndicesStats.printData(self, index)

        if self._ALL_INDICES_PLACEHOLDER in data:
            _all = data[self._ALL_INDICES_PLACEHOLDER]
            # We can name the '_all' index '_all' here (the value of ES doc field can be reserved words, it is ok)
            _all['index'] = self._ALL_KEYWORD
            # If timestamp key/value found in the root then copy it into _all indices stats too
            if self.TIMESTAMP_KEY in data:
                _all[self.TIMESTAMP_KEY] = data[self.TIMESTAMP_KEY]

            IndicesStats.printData(self, _all)
