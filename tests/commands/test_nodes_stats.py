"""Tests for our `watches nodes_stats` subcommand."""

import json
from subprocess import PIPE, Popen as popen
from secure_support import TestSecureSupport


class TestNodesStats(TestSecureSupport):
    def test_returns_json(self):
        cmd = self.appendSecurityCommands(['watches', 'nodes_stats'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 2)

    def test_returns_cluster_stats(self):
        cmd = self.appendSecurityCommands(['watches', 'nodes_stats'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('nodes' in o)
        self.assertTrue(len(o['nodes']) > 0)
        # get first node info
        first_node_key = o['nodes'].keys()[0]
        first_node_info = o['nodes'][first_node_key]
        # check there are some pool stats
        self.assertTrue('bulk' in first_node_info['thread_pool'])
        # check there is other interesting info
        self.assertTrue('jvm' in first_node_info)
        self.assertTrue('os' in first_node_info)

    def test_returns_cluster_stats_metric(self):
        cmd = self.appendSecurityCommands(['watches', 'nodes_stats', '--metric=transport,os'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o['nodes']) > 0)
        node_id = o['nodes'].keys()[0]
        node_stats = o['nodes'][node_id]
        # We required two metrics, but there is some other info available in any case,
        # thus expected size is not 2 but 7.
        self.assertTrue(len(node_stats) == 7)
        self.assertTrue('transport_address' in node_stats)
        self.assertTrue('name' in node_stats)
        self.assertTrue('timestamp' in node_stats)
        self.assertTrue('host' in node_stats)
        self.assertTrue('ip' in node_stats)
        self.assertTrue('os' in node_stats)
        self.assertTrue('transport' in node_stats)

    def test_returns_cluster_stats_filtered(self):
        cmd = self.appendSecurityCommands(['watches', 'nodes_stats', '-f nodes.*.thread_pool.bulk'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 1)
        node_id = o['nodes'].keys()[0]
        bulk = o['nodes'][node_id]['thread_pool']['bulk']
        self.assertTrue(len(bulk) == 6)
        self.assertTrue('completed' in bulk)
        self.assertTrue('rejected' in bulk)
        self.assertTrue('queue' in bulk)
        self.assertTrue('threads' in bulk)
        self.assertTrue('largest' in bulk)
        self.assertTrue('active' in bulk)

    def test_returns_cluster_stats_nested(self):
        cmd = self.appendSecurityCommands(['watches', 'nodes_stats', '--transform=nested'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)

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