from easycli import SubCommand, Argument, Mutex

from utilities.response.commands.memory import MemoryResponseHandler, SwapResponseHandler
from utilities.dataFetcher.commands.memory import MemoryDataFetcher, SwapDataFetcher
from utilities.monitoring.monitoring import Monitoring


# memory usage monitoring command
class Memory(SubCommand):
    __command__ = 'memory'
    __arguments__ = [
        # argument for monitoring usage in intervals
        Argument(
            '-i', '--interval',
            action='store',
            type=float,
            help='Interval in seconds'
        ),
        # defining mutex arguments
        Mutex(
            # argument for monitoring memory in advance mode
            Argument(
                '-a', '--advance',
                action='store_true',
                help='Memory usage advance mode'
            ),
            # argument for monitoring swap memory
            Argument(
                '-s', '--swap',
                action='store_true',
                help='Swap memory usage'
            )
        )
    ]

    def __call__(self, args):        
        swap = args.swap

        if swap:
            swap_monitor = Monitoring(data_fetcher=SwapDataFetcher, response_handler=SwapResponseHandler)
            swap_monitor.monitor(args)

        else:
            memory_monitor = Monitoring(data_fetcher=MemoryDataFetcher, response_handler=MemoryResponseHandler)
            memory_monitor.monitor(args)

