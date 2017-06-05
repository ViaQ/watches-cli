"""Tests for our `watches just_indices_stats` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from secure_support import TestSecureSupport


class TestJustIndicesStats(TestSecureSupport):

    def test_returns_index_per_line(self):
        cmd = self.appendSecurityCommands(['watches', 'just_indices_stats', '-l', '--level=indices', '--timestamp'])
        output = popen(cmd, stdout=PIPE).communicate()[0].decode('ascii')
        self.assertTrue(len(output) > 0)
        lines = 0
        for line in output.splitlines():
            lines += 1
            o = json.loads(line)
            self.assertTrue('index' in o)
            self.assertTrue('timestamp' in o)
            self.assertTrue('total' in o)
            self.assertTrue('primaries' in o)
        self.assertTrue(lines > 0)

    def test_returns_index_per_line_just__all(self):
        cmd = self.appendSecurityCommands(['watches', 'just_indices_stats', '-l'])
        output = popen(cmd, stdout=PIPE).communicate()[0].decode('ascii')
        self.assertTrue(len(output) > 0)
        lines = 0
        for line in output.splitlines():
            lines += 1
            o = json.loads(line)
            self.assertTrue('index' in o)
            self.assertTrue(o['index'] == '_all')
        # Without specifying --level=indices we get only _all index stats
        self.assertTrue(lines == 1)
