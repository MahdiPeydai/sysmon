from easycli import SubCommand, Argument

from utilities.response.commands.cpu import CpuResponseHandler 
from utilities.dataFetcher.commands import cpu
from utilities.monitoring.monitoring import Monitoring


# cpu usage monitoring subcommand
class Cpu(SubCommand):
    __command__ = 'cpu'
    __arguments__ = [
        # argument for showing usage in intervals
        Argument(
            '-i', '--interval',
            action='store',
            type=float,
            help='Interval in seconds'
        ),
        # for showing usage usage per cpu core
        Argument(
            '-p', '--percore',
            action='store_true',
            help='Cpu usage per core'
        )
    ]

    def __call__(self, args):
        cpu_monitor = Monitoring(data_fetcher=cpu.CpuDataFetcher, response_handler=CpuResponseHandler)
        cpu_monitor.monitor(args)
