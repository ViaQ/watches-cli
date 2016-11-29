"""Tests for our `watches cluster_state` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestClusterState(TestCase):
    def test_returns_json(self):
        output = popen(['watches', 'cluster_state'], stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 9)

    def test_returns_cluster_state(self):
        output = popen(['watches', 'cluster_state'], stdout=PIPE).communicate()[0]
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
