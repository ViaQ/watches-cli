

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
    def appendSecurityCommands(list):

        #security_enabled = "true"
        security_enabled = os.environ["IS_ES_SECURED"]

        if "true" == security_enabled:
            list.append('--url=' + TestSecureSupport._sec['--url'])
            list.append('--cacert=' + TestSecureSupport._sec['--cacert'])
            list.append('--cert=' + TestSecureSupport._sec['--cert'])
            list.append('--key=' + TestSecureSupport._sec['--key'])

        # print "Secured command?", list
        return list

    @staticmethod
    def appendOnlyCAcert(list):

        # security_enabled = "true"
        security_enabled = os.environ["IS_ES_SECURED"]

        if "true" == security_enabled:
            list.append('--url=' + TestSecureSupport._sec['--url'])
            list.append('--cacert=' + TestSecureSupport._sec['--cacert'])

        # print "Secured command?", list
        return list

    @staticmethod
    def options_from_list(list):
        # for i in list:
        #     item = i.split('=')
        #     o[item[0]] = item[1]
        o = dict(item.split("=", 1) for item in list)
        return o
