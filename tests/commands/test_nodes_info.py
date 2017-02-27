"""Tests for our `watches nodes_info` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from secure_support import TestSecureSupport


class TestNodesInfo(TestSecureSupport):
    def test_returns_json(self):
        cmd = self.appendSecurityCommands(['watches', 'nodes_info'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 2)

    def test_returns_nodes_info(self):
        cmd = self.appendSecurityCommands(['watches', 'nodes_info'])
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
        self.assertTrue('plugins' in first_node_info)

    def test_returns_nodes_info_metric(self):
        cmd = self.appendSecurityCommands(['watches', 'nodes_info', '--metric=http,process'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o['nodes']) > 0)
        node_id = o['nodes'].keys()[0]
        node_info = o['nodes'][node_id]
        # We required two metrics, but there is some other info available in any case,
        # thus expected size is not 2 but 9.
        self.assertTrue(len(node_info) == 9)
        self.assertTrue('transport_address' in node_info)
        self.assertTrue('http' in node_info)
        self.assertTrue('name' in node_info)
        self.assertTrue('process' in node_info)
        self.assertTrue('ip' in node_info)
        self.assertTrue('host' in node_info)
        self.assertTrue('version' in node_info)
        self.assertTrue('build' in node_info)
        self.assertTrue('http_address' in node_info)

    def test_returns_nodes_info_filtered(self):
        cmd = self.appendSecurityCommands(['watches', 'nodes_info', '-f nodes.*.thread_pool.bulk'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 1)
        node_id = o['nodes'].keys()[0]
        bulk = o['nodes'][node_id]['thread_pool']['bulk']
        self.assertTrue(len(bulk) == 4)
        self.assertTrue('min' in bulk)
        self.assertTrue('max' in bulk)
        self.assertTrue('type' in bulk)
        self.assertTrue('queue_size' in bulk)

    def test_returns_nodes_info_nested(self):
        cmd = self.appendSecurityCommands(['watches', 'nodes_info', '--transform=nested'])
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