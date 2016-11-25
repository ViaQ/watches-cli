"""Tests for our `watches indices_stats` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase
from elasticsearch import Elasticsearch


class TestIndicesStats(TestCase):
    def test_returns_multiple_lines(self):
        output = popen(['watches', 'indices_stats'], stdout=PIPE).communicate()[0]
        lines = output.split('\n')
        self.assertTrue(len(lines) != 1)

    def test_returns_nodes_info(self):

        # Unless we index some data to cluster the output does not contain "shards" part
        # TODO: make ES client configurable, now it is hardcoded to default: 'http://localhost:9200'
        es = Elasticsearch()
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409, refresh=True)

        output = popen(['watches', 'indices_stats', '--level=shards'], stdout=PIPE).communicate()[0]
        self.assertTrue('"primaries"' in output)
        self.assertTrue('"indices"' in output)
        self.assertTrue('"shards"' in output)