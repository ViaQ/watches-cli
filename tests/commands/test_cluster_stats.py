"""Tests for our `watches cluster_stats` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestClusterStats(TestCase):
    def test_returns_multiple_lines(self):
        output = popen(['watches', 'cluster_stats'], stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 5)

    def test_returns_cluster_stats(self):
        output = popen(['watches', 'cluster_stats'], stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('timestamp' in o)
        self.assertTrue('nodes' in o)

        nodes_count = o['nodes']['count']
        self.assertTrue('total' in nodes_count)
        self.assertTrue('client' in nodes_count)
        self.assertTrue('data_only' in nodes_count)
        self.assertTrue('master_only' in nodes_count)
        self.assertTrue('master_data' in nodes_count)

        nodes_os = o['nodes']['os']
        self.assertTrue('mem' in nodes_os)
        self.assertTrue('allocated_processors' in nodes_os)
        self.assertTrue('available_processors' in nodes_os)

        self.assertTrue('status' in o)
        self.assertTrue('indices' in o)

        indices = o['indices']
        self.assertTrue('count' in indices)
        self.assertTrue('fielddata' in indices)
        self.assertTrue('docs' in indices)
        self.assertTrue('segments' in indices)
        self.assertTrue('shards' in indices)
        self.assertTrue('store' in indices)
