"""Tests for our `watches cluster_state` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from secure_support import TestSecureSupport
from watches.util import ESClientProducer


class TestClusterState(TestSecureSupport):
    def test_returns_json(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_state'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 9)

    def test_returns_cluster_state_local(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_state', '--local'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 9)

    def test_returns_cluster_state(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_state'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('state_uuid' in o)
        self.assertTrue('master_node' in o)
        self.assertTrue('nodes' in o)
        self.assertTrue('version' in o)
        self.assertTrue('blocks' in o)
        self.assertTrue('routing_table' in o)
        self.assertTrue('routing_nodes' in o)
        self.assertTrue('metadata' in o)

        metadata = o['metadata']
        self.assertTrue('cluster_uuid' in metadata)
        self.assertTrue('templates' in metadata)
        self.assertTrue('indices' in metadata)

    def test_returns_cluster_state_metric_and_index(self):
        es = ESClientProducer.create_client(
            self.options_from_list(self.appendSecurityCommands([]))
        )
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409, refresh=True)

        cmd = self.appendSecurityCommands(['watches', 'cluster_state', '--metric=metadata', '--index=i'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 2)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('metadata' in o)
        self.assertTrue('i' in o['metadata']['indices'])

    def test_returns_cluster_state_filtered(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_state', '-f cluster_name', '-f master_node'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 2)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('master_node' in o)

    def test_returns_cluster_state_nested(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_state', '--transform=nested'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)

        self.assertTrue('metadata' in o)
        self.assertTrue('indices' in o['metadata'])
        indices = o['metadata']['indices']

        # Indices is an array
        self.assertTrue(isinstance(indices, list))
        self.assertTrue(len(indices) > 0)

        for index in indices:
            # Each item in indices array must be dictionary
            self.assertTrue(isinstance(index, dict))

            # Each item must contain 'index' field which is expected to hold index name (thus string type)
            self.assertTrue('index' in index)
            self.assertTrue(isinstance(index['index'], basestring))

        # Nodes is an array
        self.assertTrue('nodes' in o)
        nodes = o['nodes']
        self.assertTrue(isinstance(nodes, list))
        self.assertTrue(len(nodes) > 0)

        for node in nodes:
            # Each item in nodes array must be dictionary
            self.assertTrue(isinstance(node, dict))
            # Each item must contain 'node' field which is expected to hold node hash id (thus string type)
            self.assertTrue('node' in node)
            self.assertTrue(isinstance(node['node'], basestring))

        # Routing table indices
        self.assertTrue('routing_table' in o)
        self.assertTrue('indices' in o['routing_table'])
        indices = o['routing_table']['indices']
        self.assertTrue(isinstance(indices, list))
        self.assertTrue(len(indices) > 0)
        for index in indices:
            self.assertTrue(isinstance(index, dict))
            self.assertTrue('index' in index)
            self.assertTrue(isinstance(index['index'], basestring))
            self.assertTrue('shards' in index)
            self.assertTrue(isinstance(index['shards'], list))
            self.assertTrue(len(index['shards']) > 0)
            for shard in index['shards']:
                self.assertTrue(isinstance(shard, dict))
                self.assertTrue('shard' in shard)
                self.assertTrue(isinstance(shard['shard'], int))

        # Routing nodes nodes
        self.assertTrue('routing_nodes' in o)
        self.assertTrue('nodes' in o['routing_nodes'])
        nodes = o['routing_nodes']['nodes']
        self.assertTrue(isinstance(nodes, list))
        self.assertTrue(len(nodes) > 0)
        for node in nodes:
            self.assertTrue('node' in node)
            self.assertTrue('shard' in node)
            self.assertTrue('index' in node)