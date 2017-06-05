"""
watches

Usage:
  watches cluster_health     [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--transform=TYPE] [--local --index=INDEX --level=LEVEL]
  watches cluster_state      [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--transform=TYPE] [--local --index=INDEX --metric=METRIC]
  watches cluster_stats      [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--transform=TYPE]
  watches nodes_stats        [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--transform=TYPE] [--metric=METRIC]
  watches nodes_info         [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--transform=TYPE] [--node_id=NODE_ID --metric=METRIC]
  watches indices_stats      [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--transform=TYPE] [--level=LEVEL --index=INDEX]
  watches nodes_hotthreads   [-i=INTERVAL -d=DURATION --url=URL -bsv] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--node_id=NODE_ID --threads=THREADS --delay=DELAY --type=TYPE]
  watches just_nodes_stats   [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--metric=METRIC]
  watches just_indices_stats [-i=INTERVAL -d=DURATION --url=URL -bltsv -f=FILTER...] [(--cacert=CACERT --cert=CERT --key=KEY) | (--cacert=CACERT)] [(--username=USERNAME --password=PASSWORD)] [--header=HEADER...] [--level=LEVEL --index=INDEX]
  watches -h
  watches --version

Options:
  -d=DURATION, --duration=DURATION   How long the watches should run in seconds. Use value '-1' to run forever. [default: 0].
  -i=INTERVAL, --interval=INTERVAL   Interval between data retrievals. Apply if 'duration' > 0. [default: 3].
  --url=URL           URL of ES node HTTP endpoint [default: http://localhost:9200].
  -b                  Disable python output buffering (not recommended for production use).
  -l                  Single line output (no pretty-print JSON formatting).
  -t, --timestamp     Add timestamp field to data. The value is local datetime converted to UTC in ISO 8601 format.
  -s, --sniff         Turn on sniffing.
  -v, --verbose       Print more debug info: input options, ... etc.
  -f=FILTER, --filter_path=FILTER   Filter returned JSON (see http://elasticsearch-py.readthedocs.io/en/master/api.html#response-filtering)
  --username=USERNAME Username to authenticate with
  --password=PASSWORD Password to authenticate with
  --cacert=CACERT     Path to Certification Authority Certificate pem file
  --cert=CERT         Path to Client Certificate pem file
  --key=KEY           Path to Client Key pem file
  --level=LEVEL       Aggregation level of returned data, valid options: node/cluster, indices and shards [default: cluster].
  --local             Return the local node information instead of master node [default: false].
  --node_id=NODE_ID   A comma-separated list of node IDs or names to limit the returned information; use `_local` to return information from local node you're connecting to [default: ].
  --index=INDEX       A comma-separated list of index names; use `_all` or empty string to perform the operation on all indices.
  --metric=METRIC     A comma-separated list of metric names; use `_all` or empty string to perform the operation for all metrics.
  --threads=THREADS   Specify the number of threads to provide information for.
  --delay=DELAY       Delay (interval) to do the second sampling of threads.
  --type=TYPE         The type of threads to sample (default: cpu), valid choices are: 'cpu', 'wait', 'block'.
  --transform=TYPE    Transform JSON response (see online doc for more details). Valid choices: 'nested'.
  -h, --help          Show this screen.
  --version           Show version.
  --header=HEADER     Custom HTTP header to add to the request (e.g. --header="X-Proxy-Remote-User: username")

Examples:
  # Get cluster health from specified HTTP endpoint with added "timestamp" field in the response
  $ watches cluster_health --timestamp --url=http://127.0.0.1:9200

  # Get cluster health every 1 second, run forever until process is terminated
  $ watches cluster_health --interval=1 --duration=-1

  # Get cluster health every 1 second during next 10 seconds and use sniffing
  $ watches cluster_health --interval=1 --duration=10 --sniff

  # Alternatively, using short option notation
  $ watches cluster_health -i 1 -d 10 -s

  # Get cluster health from secured node
  $ watches cluster_health \
      --url=https://localhots:9200 \
      --cacert /tmp/search-guard-ssl/example-pki-scripts/ca/chain-ca.pem \
      --cert /tmp/search-guard-ssl/example-pki-scripts/kirk.crt.pem \
      --key /tmp/search-guard-ssl/example-pki-scripts/kirk.key.pem

  # Filter cluster health for status fields
  $ watches cluster_health --level=shards -f status -f indices.*.status -f indices.*.shards.*.status

Notice:
  Option --filter_path works under original context for commands 'just_nodes_stats' and 'just_indices_stats'.
  For example, if command 'just_indices_stats' is called the 'indices_stats' command is executed first, then
  --filter_path option is applied and only then the result data is transformed into 'just_indices_stats' output.

Help:
  For help using this tool, please open an issue on the GitHub repository:
  https://github.com/ViaQ/watches-cli
"""


from inspect import getmembers, isclass

from docopt import docopt
import time
import os
import signal
import sys
import inspect
import calendar
import logging

from . import __version__ as VERSION


def sigterm_handler(_signo, _stack_frame):
    sys.stdout.flush()


def main():
    """Main CLI entrypoint."""

    # Make sure stdout buffer is flushed on these signals
    signal.signal(signal.SIGINT,  sigterm_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)

    import watches.commands
    commands = {}
    for k, v in inspect.getmembers(sys.modules["watches.commands"], inspect.isclass):
        commands[k] = v
    options = docopt(__doc__, version=VERSION)

    # Turn off buffering, see #20
    if options['-b']:
        # buffsize = 1 should perform better then 0 while still good option for 'tail -f ...'
        unbuffered = os.fdopen(sys.stdout.fileno(), "w", 1)
        sys.stdout = unbuffered

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.items():
        if k in commands and v:
            module = commands[k]
            commands = getmembers(module, isclass)
            # command = [command[1] for command in commands if command[0] != 'Base'][0]
            # command = command(options)
            command = module(options)

            duration = int(options['--duration'])
            interval = int(options['--interval'])
            startsec = calendar.timegm(time.gmtime())
            endsec = (startsec + duration)

            while True:
                execute(command)
                if duration == 0:
                    break
                actualsec = calendar.timegm(time.gmtime())
                # print duration, interval, startsec, actualsec, endsec
                if duration > -1 and (actualsec + interval) >= endsec:
                    break
                time.sleep(interval)


def execute(command):
    """
    Execute the command. If any exceptions occur they are caught and logged.
    :param command:
    :return:
    """
    try:
        command.run()
    except Exception:
        # Is this acceptable way of logging exceptions?
        # http://stackoverflow.com/a/4508872
        logging.exception('')
        pass

