"""Tests for our `watches indices_stats` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from secure_support import TestSecureSupport
from watches.util import ESClientProducer


class TestIndicesStats(TestSecureSupport):
    def test_returns_json(self):
        cmd = self.appendSecurityCommands(['watches', 'indices_stats'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 2)

    def test_returns_nodes_info_cluster_level(self):

        # Unless we index some data to cluster the output does not contain "shards" part
        es = ESClientProducer.create_client(
            self.options_from_list(self.appendSecurityCommands([]))
        )
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409, refresh=True)

        cmd = self.appendSecurityCommands(['watches', 'indices_stats'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 2)
        self.assertTrue('_all' in o)
        self.assertTrue('_shards' in o)

    def test_returns_nodes_info_shards_level(self):

        # Unless we index some data to cluster the output does not contain "shards" part
        es = ESClientProducer.create_client(
            self.options_from_list(self.appendSecurityCommands([]))
        )
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409, refresh=True)

        cmd = self.appendSecurityCommands(['watches', 'indices_stats', '--level=shards'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
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

    def test_returns_nodes_info_shards_level_filtered(self):
        cmd = self.appendSecurityCommands(['watches', 'indices_stats', '-f _all.total.docs'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        docs = o['_all']['total']['docs']
        self.assertTrue(len(docs) == 2)
        self.assertTrue('count' in docs)
        self.assertTrue('deleted' in docs)

    def test_returns_nodes_info_shards_nested(self):
        cmd = self.appendSecurityCommands(['watches', 'indices_stats', '--index=i', '--level=shards', '--transform=nested'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)

        # Indices is an array
        self.assertTrue('indices' in o)
        indices = o['indices']
        self.assertTrue(isinstance(indices, list))
        self.assertTrue(len(indices) > 0)

        for index in indices:
            # Each item in indices array must be dictionary
            self.assertTrue(isinstance(index, dict))
            # Each item must contain 'index' field which is expected to hold index name (thus string type)
            self.assertTrue('index' in index)
            self.assertTrue(isinstance(index['index'], basestring))

            self.assertTrue('shards' in index)
            self.assertTrue(isinstance(index['shards'], list))
            self.assertTrue(len(index['shards']) > 0)

            for shard in index['shards']:
                self.assertTrue('shard' in shard)
                self.assertTrue(isinstance(shard['shard'], int))