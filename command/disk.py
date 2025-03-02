from easycli import SubCommand, Argument

from utilities.response.commands.disk import DiskResponseHandler, DiskIOResponseHandler
from utilities.dataFetcher.commands.disk import DiskDataFetcher, DiskIODataFetcher
from utilities.monitoring.monitoring import Monitoring


# Disk usage monitoring command
class Disk(SubCommand):
    __command__ = 'disk'
    __arguments__ = [
        # argument for monitoring usage in intervals
        Argument(
            '-i', '--interval',
            action='store',
            type=float,
            help='Interval in seconds, Implies --io'
        ),
        # argument for monitoring disk I/O
        Argument(
            '--io',
            action='store_true',
            help='Disk I/O'
        ),
        # argument for monitoring I/O per disk
        Argument(
            '-p', '--perdisk',
            action="store_true",
            help='I/O per disk, Implies --io'
        )
    ]

    def __call__(self, args):
        interval = args.interval
        perdisk = args.perdisk
        inputOutput = args.io

        if inputOutput or perdisk or interval: # handling monitoring I/O    
            cpu_monitor = Monitoring(data_fetcher=DiskIODataFetcher, response_handler=DiskIOResponseHandler)
            cpu_monitor.monitor(args)
        
        else:
            cpu_monitor = Monitoring(data_fetcher=DiskDataFetcher, response_handler=DiskResponseHandler)
            cpu_monitor.monitor(args)
