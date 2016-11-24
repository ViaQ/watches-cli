"""Tests for our `watches cluster_state` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestClusterState(TestCase):
    def test_returns_multiple_lines(self):
        output = popen(['watches', 'cluster_state'], stdout=PIPE).communicate()[0]
        lines = output.split('\n')
        self.assertTrue(len(lines) != 1)

    def test_returns_cluster_state(self):
        output = popen(['watches', 'cluster_state'], stdout=PIPE).communicate()[0]
        self.assertTrue('state_uuid' in output)
        self.assertTrue('cluster_name' in output)
        self.assertTrue('master_node' in output)
        self.assertTrue('version' in output)

        self.assertTrue('nodes' in output)
        self.assertTrue('metadata' in output)
        self.assertTrue('cluster_uuid' in output)
        self.assertTrue('templates' in output)
        self.assertTrue('indices' in output)