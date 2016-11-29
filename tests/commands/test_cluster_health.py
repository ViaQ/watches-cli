"""Tests for our `watches cluster_health` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from unittest import TestCase
from elasticsearch import Elasticsearch


class TestClusterHealth(TestCase):
    def test_returns_json(self):
        output = popen(['watches', 'cluster_health'], stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 15)
        self.assertTrue('status' in o)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('number_of_nodes' in o)


    def test_returns_cluster_health_with_sniffing(self):
        output = popen(['watches', 'cluster_health', '--sniff'], stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 15)
        self.assertTrue('status' in o)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('number_of_nodes' in o)

    def test_returns_cluster_health_with_verbose(self):
        output = popen(['watches', 'cluster_health', '--verbose'], stdout=PIPE).communicate()[0]
        # Unless we index some data to cluster we can only check the indices field is present
        self.assertTrue('Supplied options' in output)

    def test_returns_cluster_health_with_timestamp(self):
        output = popen(['watches', 'cluster_health', '--timestamp'], stdout=PIPE).communicate()[0]
        # Unless we index some data to cluster we can only check the indices field is present
        o = json.loads(output)
        self.assertTrue(len(o) == 16)
        self.assertTrue('timestamp' in o)

    def test_returns_cluster_health(self):
        output = popen(['watches', 'cluster_health'], stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('number_of_nodes' in o)
        self.assertTrue('number_of_data_nodes' in o)
        self.assertTrue('active_primary_shards' in o)
        self.assertTrue('active_shards' in o)
        self.assertTrue('relocating_shards' in o)
        self.assertTrue('initializing_shards' in o)
        self.assertTrue('unassigned_shards' in o)
        # These are not found in object unless we explicitly use option
        self.assertTrue('indices' not in o)
        self.assertTrue('shards' not in o)
        self.assertTrue('timestamp' not in o)

    def test_returns_cluster_health_with_indices(self):
        output = popen(['watches', 'cluster_health', '--level=indices'], stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('indices' in o)
        self.assertTrue('shards' not in o)

    def test_returns_cluster_health_with_shards(self):

        # Unless we index some data to cluster the output does not contain "shards" part
        # TODO: make ES client configurable, now it is hardcoded to default: 'http://localhost:9200'
        es = Elasticsearch()
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409, refresh=True)

        output = popen(['watches', 'cluster_health', '--level=shards'], stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('indices' in o)
        self.assertTrue('shards' in o['indices']['i'])