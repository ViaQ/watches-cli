"""Tests for our `watches nodes_info` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestNodesInfo(TestCase):
    def test_returns_multiple_lines(self):
        output = popen(['watches', 'nodes_info'], stdout=PIPE).communicate()[0]
        lines = output.split('\n')
        self.assertTrue(len(lines) != 1)

    def test_returns_nodes_info(self):
        output = popen(['watches', 'nodes_info'], stdout=PIPE).communicate()[0]
        self.assertTrue('cluster_name' in output)
        self.assertTrue('nodes' in output)