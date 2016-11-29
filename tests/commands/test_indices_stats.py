"""Tests for our `watches indices_stats` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from unittest import TestCase
from elasticsearch import Elasticsearch


class TestIndicesStats(TestCase):
    def test_returns_json(self):
        output = popen(['watches', 'indices_stats'], stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 2)

    def test_returns_nodes_info_cluster_level(self):

        # Unless we index some data to cluster the output does not contain "shards" part
        # TODO: make ES client configurable, now it is hardcoded to default: 'http://localhost:9200'
        es = Elasticsearch()
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409, refresh=True)

        output = popen(['watches', 'indices_stats',], stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 2)
        self.assertTrue('_all' in o)
        self.assertTrue('_shards' in o)

    def test_returns_nodes_info_shards_level(self):

        # Unless we index some data to cluster the output does not contain "shards" part
        # TODO: make ES client configurable, now it is hardcoded to default: 'http://localhost:9200'
        es = Elasticsearch()
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409, refresh=True)

        output = popen(['watches', 'indices_stats', '--level=shards'], stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 3)
        self.assertTrue('_all' in o)
        self.assertTrue('_shards' in o)
        self.assertTrue('indices' in o)

        self.assertTrue('total' in o['indices']['i'])
        self.assertTrue('primaries' in o['indices']['i'])
        self.assertTrue('shards' in o['indices']['i'])

        _all = o['_all']
        self.assertTrue('total' in _all)
        self.assertTrue('primaries' in _all)