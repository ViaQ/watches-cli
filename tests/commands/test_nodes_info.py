"""Tests for our `watches nodes_info` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestNodesInfo(TestCase):
    def test_returns_json(self):
        output = popen(['watches', 'nodes_info'], stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 2)

    def test_returns_nodes_info(self):
        output = popen(['watches', 'nodes_info'], stdout=PIPE).communicate()[0]
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
