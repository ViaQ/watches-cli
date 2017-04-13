

import os
from unittest import TestCase


class TestSecureSupport(TestCase):
    """
    Support for tests running in secured context.
    """

    # Values compatible with setup script
    _sec = {
        '--url': 'https://localhost:9200',
        '--cacert': '/tmp/search-guard-ssl/example-pki-scripts/ca/chain-ca.pem',
        '--cert': '/tmp/search-guard-ssl/example-pki-scripts/kirk.crt.pem',
        '--key': '/tmp/search-guard-ssl/example-pki-scripts/kirk.key.pem'
    }

    @staticmethod
    def appendSecurityCommands(params):

        # security_enabled = "true"
        security_enabled = os.environ["IS_ES_SECURED"]

        if "true" == security_enabled:
            params.append('--url=' + TestSecureSupport._sec['--url'])
            params.append('--cacert=' + TestSecureSupport._sec['--cacert'])
            params.append('--cert=' + TestSecureSupport._sec['--cert'])
            params.append('--key=' + TestSecureSupport._sec['--key'])

        # print "Secured command?", params
        return params

    @staticmethod
    def appendOnlyCAcert(params):

        # security_enabled = "true"
        security_enabled = os.environ["IS_ES_SECURED"]

        if "true" == security_enabled:
            params.append('--url=' + TestSecureSupport._sec['--url'])
            params.append('--cacert=' + TestSecureSupport._sec['--cacert'])

        # print "Secured command?", params
        return params

    @staticmethod
    def options_from_list(params):
        # for i in params:
        #     item = i.split('=')
        #     o[item[0]] = item[1]
        o = dict(item.split("=", 1) for item in params)
        return o
