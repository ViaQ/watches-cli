"""Tests for our `watches cluster_health` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from secure_support import TestSecureSupport
from watches.util import ESClientProducer


class TestClusterHealth(TestSecureSupport):
    username_password = ['--username', 'kirk', '--password', 'kirk']

    def test_returns_json(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        self.assertTrue(output.count("\n") > 1)
        o = json.loads(output)
        self.assertTrue(len(o) == 15)
        self.assertTrue('status' in o)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('number_of_nodes' in o)

    def test_returns_single_line_json(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '-l'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        self.assertTrue(output.count("\n") == 1)
        self.assertTrue('status' in output)
        self.assertTrue('cluster_name' in output)
        self.assertTrue('number_of_nodes' in output)

    # Test unbuffered output, see #20
    # In fact we only test that the code can pass through this without issues
    # but we do not test the effect of the buffer size. This is at least useful
    # when testing against different versions of Python ('cos it depends on low level API).
    def test_returns_single_line_unbuffered_json(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '-lb'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        self.assertTrue(output.count("\n") == 1)
        self.assertTrue('status' in output)
        self.assertTrue('cluster_name' in output)
        self.assertTrue('number_of_nodes' in output)

    def test_returns_cluster_health_with_sniffing(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--sniff'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 15)
        self.assertTrue('status' in o)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('number_of_nodes' in o)

    def test_returns_cluster_health_with_verbose(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--verbose'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        # Unless we index some data to cluster we can only check the indices field is present
        self.assertTrue('Supplied options' in output)

    def test_returns_cluster_health_with_timestamp(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--timestamp'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        # Unless we index some data to cluster we can only check the indices field is present
        o = json.loads(output)
        self.assertTrue(len(o) == 16)
        self.assertTrue('timestamp' in o)

    def test_returns_cluster_health(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('number_of_nodes' in o)
        self.assertTrue('number_of_data_nodes' in o)
        self.assertTrue('active_primary_shards' in o)
        self.assertTrue('active_shards' in o)
        self.assertTrue('relocating_shards' in o)
        self.assertTrue('initializing_shards' in o)
        self.assertTrue('unassigned_shards' in o)
        # These are not found in object unless we explicitly use option
        self.assertTrue('indices' not in o)
        self.assertTrue('shards' not in o)
        self.assertTrue('timestamp' not in o)

    def test_returns_cluster_health_with_indices(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--level=indices'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('indices' in o)
        self.assertTrue('shards' not in o)

    def test_returns_cluster_health_with_shards(self):
        es = ESClientProducer.create_client(
            self.options_from_list(self.appendSecurityCommands([]))
        )
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409, refresh=True)

        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--level=shards'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('indices' in o)
        self.assertTrue('shards' in o['indices']['i'])

    def test_returns_cluster_health_with_shards_filtered(self):
        es = ESClientProducer.create_client(
            self.options_from_list(self.appendSecurityCommands([]))
        )
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409, refresh=True)

        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--level=shards',
                                           '-f status', '-f *.*.status', '-f indices.*.shards.*.status'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)

        self.assertTrue(len(o) == 2)
        self.assertTrue('status' in o)
        self.assertTrue('indices' in o)

        self.assertTrue(len(o['indices']['i']) == 2)
        self.assertTrue('status' in o['indices']['i'])
        self.assertTrue('shards' in o['indices']['i'])

        self.assertTrue(len(o['indices']['i']['shards']['0']) == 1)
        self.assertTrue('status' in o['indices']['i']['shards']['0'])

    def test_ca_cert_only(self):
        cmd = self.appendOnlyCAcert(['watches', 'cluster_health'])
        cmd.extend(TestClusterHealth.username_password)
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 15)
        self.assertTrue('status' in o)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('number_of_nodes' in o)

    def test_ca_cert_only_and_headers(self):
        cmd = self.appendOnlyCAcert(['watches', 'cluster_health'])
        cmd.extend(TestClusterHealth.username_password)
        cmd.extend(['--header', 'X-Foo: foo', '--header', 'X-Bar: bar'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 15)
        self.assertTrue('status' in o)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('number_of_nodes' in o)

   # negative tests to see if we get Usage: message for bogus arguments
    def test_username_no_password(self):
        cmd = self.appendOnlyCAcert(['watches', 'cluster_health'])
        cmd.extend(['--username', 'junk'])
        output = popen(cmd, stderr=PIPE).communicate()[1]
        self.assertTrue('Usage:' in output)

    def test_password_no_username(self):
        cmd = self.appendOnlyCAcert(['watches', 'cluster_health'])
        cmd.extend(['--password', 'junk'])
        output = popen(cmd, stderr=PIPE).communicate()[1]
        self.assertTrue('Usage:' in output)

    def test_cert_no_key(self):
        cmd = self.appendOnlyCAcert(['watches', 'cluster_health'])
        cmd.extend(['--cert', './junk'])
        output = popen(cmd, stderr=PIPE).communicate()[1]
        self.assertTrue('Usage:' in output)

    def test_key_no_cert(self):
        cmd = self.appendOnlyCAcert(['watches', 'cluster_health'])
        cmd.extend(['--key', './junk'])
        output = popen(cmd, stderr=PIPE).communicate()[1]
        self.assertTrue('Usage:' in output)

    def test_bogus_transform_value(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--transform=bogus'])
        output, errout = popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
        self.assertRegexpMatches(errout, '(?ms)ERROR:.*RuntimeError: Unsupported transform type')

    def test_returns_cluster_health_nested(self):
        es = ESClientProducer.create_client(
            self.options_from_list(self.appendSecurityCommands([]))
        )
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409, refresh=True)

        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--transform=nested', '--level=shards'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)

        # Indices is an array
        self.assertTrue('indices' in o)
        indices = o['indices']
        self.assertTrue(isinstance(indices, list))
        self.assertTrue(len(indices) > 0)

        for index in indices:
            # Each item in indices array must be dictionary
            self.assertTrue(isinstance(index, dict))

            # Each item must contain 'index' field which is expected to hold index name (thus string type)
            self.assertTrue('index' in index)
            self.assertTrue(isinstance(index['index'], basestring))

            # Each index must contains shards array
            self.assertTrue('shards' in index)
            shards = index['shards']
            self.assertTrue(isinstance(shards, list))

            for shard in shards:
                # Each item in shards array must be dictionary
                self.assertTrue(isinstance(shard, dict))
                self.assertTrue('shard' in shard)
                # shard id is int type, not string
                self.assertTrue(isinstance(shard['shard'], int))
