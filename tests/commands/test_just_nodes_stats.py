"""Tests for our `watches just_nodes_stats` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from secure_support import TestSecureSupport


class TestJustNodesStats(TestSecureSupport):

    def test_returns_node_per_line(self):
        cmd = self.appendSecurityCommands(['watches', 'just_nodes_stats', '-l', '--timestamp'])
        output = popen(cmd, stdout=PIPE).communicate()[0].decode('ascii')
        self.assertTrue(len(output) > 0)
        lines = 0
        for line in output.splitlines():
            lines += 1
            o = json.loads(line)
            self.assertTrue('node' in o)
            self.assertTrue('timestamp' in o)
            self.assertTrue('thread_pool' in o)
            self.assertTrue('http' in o)
            self.assertTrue('process' in o)
            self.assertTrue('breakers' in o)
            self.assertTrue('fs' in o)
            self.assertTrue('jvm' in o)
            self.assertTrue('indices' in o)
            self.assertTrue('os' in o)
            self.assertTrue('transport' in o)
        self.assertTrue(lines > 0)
