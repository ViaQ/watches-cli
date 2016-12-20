"""Tests for our `watches nodes_hotthreads` subcommand."""


from subprocess import PIPE, Popen as popen
from secure_support import TestSecureSupport


class TestNodesHotThreads(TestSecureSupport):
    def test_returns_data(self):
        cmd = self.appendSecurityCommands(['watches', 'nodes_hotthreads', '--threads', '10'])
        o = popen(cmd, stdout=PIPE).communicate()[0]
        self.assertTrue(len(o) > 0)
        self.assertTrue('Hot threads' in o)
        self.assertTrue('interval=500ms, busiestThreads=10' in o)