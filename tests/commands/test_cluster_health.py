"""Tests for our `watches cluster_health` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase
from elasticsearch import Elasticsearch


class TestClusterHealth(TestCase):
    def test_returns_multiple_lines(self):
        output = popen(['watches', 'cluster_health'], stdout=PIPE).communicate()[0]
        lines = output.split('\n')
        self.assertTrue(len(lines) != 1)

    def test_returns_cluster_health_with_verbose(self):
        output = popen(['watches', 'cluster_health', '--verbose'], stdout=PIPE).communicate()[0]
        # Unless we index some data to cluster we can only check the indices field is present
        self.assertTrue('Supplied options' in output)

    def test_returns_cluster_health_with_timestamp(self):
        output = popen(['watches', 'cluster_health', '--timestamp'], stdout=PIPE).communicate()[0]
        # Unless we index some data to cluster we can only check the indices field is present
        self.assertTrue('"timestamp"' in output)

    def test_returns_cluster_health(self):
        output = popen(['watches', 'cluster_health'], stdout=PIPE).communicate()[0]
        self.assertTrue('cluster_name' in output)
        self.assertTrue('number_of_nodes' in output)
        self.assertTrue('number_of_data_nodes' in output)
        self.assertTrue('active_primary_shards' in output)
        self.assertTrue('active_shards' in output)
        self.assertTrue('relocating_shards' in output)
        self.assertTrue('initializing_shards' in output)
        self.assertTrue('unassigned_shards' in output)
        self.assertFalse('"indices"' in output)
        self.assertFalse('"shards"' in output)
        self.assertFalse('"timestamp"' in output)

    def test_returns_cluster_health_with_indices(self):
        output = popen(['watches', 'cluster_health', '--level=indices'], stdout=PIPE).communicate()[0]
        self.assertTrue('"indices":' in output)
        self.assertFalse('"shards"' in output)

    def test_returns_cluster_health_with_shards(self):
        output = popen(['watches', 'cluster_health', '--level=shards'], stdout=PIPE).communicate()[0]
        # Unless we index some data to cluster the output does not contain "shards" part
        # TODO: make ES client configurable, now it is hardcoded to default: 'http://localhost:9200'
        es = Elasticsearch()
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409)
        self.assertTrue('"indices":' in output)
        self.assertTrue('"shards"' in output)