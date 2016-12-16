"""Provider of Elasticsearch client."""

from elasticsearch import Elasticsearch

def create_client(options):
    """Produces a new Elasticsearch client according to provided options."""

    user_kwargs = {}

    if "--url" in options:
        user_kwargs.update({
            'hosts': options["--url"]
        })

    if "--username" in options or "--password" in options:
        http_auth_str = "://{}:{}@".format(options["--username"], options["--password"])
        url = user_kwargs.get('hosts', 'http://localhost:9200')
        user_kwargs['hosts'] = url.replace('://', http_auth_str)

    # "true" is not translated to native True value ?
    if "--sniff" in options and "true" == options["--sniff"]:
        user_kwargs.update({
            # sniff before doing anything
            "sniff_on_start": True,
            # refresh nodes after a node fails to respond
            "sniff_on_connection_fail": True,
            # and also every 60 seconds
            "sniffer_timeout": 60
        })

    if "--cacert" in options and options['--cacert']:
        #see if the value is a string or a list
        if isinstance(options['--cacert'], basestring):
            cacert = options['--cacert']
        else: # assume list
            cacert = options['--cacert'][0]
        # because we mention --cacert in two places in the docopt, it automatically
        # converts to a list - we just take the first one
        user_kwargs.update({
            "ca_certs": cacert
        })

    # if --cert or --key is provided, both must be provided, and --cacert too
    if "--cert" in options or "--key" in options:
        user_kwargs.update({
            "client_cert": options["--cert"],
            "client_key": options["--key"]
        })

    # convert from list to dict
    headers = {}
    for hdr in options.get('--header', []):
        k,v = hdr.split(':', 1)
        headers[k] = v.lstrip()
    if headers:
         user_kwargs.update({
            "headers": headers
        })

    es = Elasticsearch(**user_kwargs)

    return es
