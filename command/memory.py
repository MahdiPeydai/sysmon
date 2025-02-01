import psutil
import time
import sys

from easycli import SubCommand, Argument

from utilities.response.command.memory import MemoryUsageResponse


class Memory(SubCommand):
    __command__ = 'memory'
    __arguments__ = [
        Argument(
            '-i', '--interval',
            action='store',
            type=float,
            help='Interval in seconds'
        ),
        Argument(
            '-a', '--advance',
            action='store_true',
            help='Memory usage advance mode'
        ),
        Argument(
            '-s', '--swap',
            action='store_true',
            help='Swap memory usage'
        )
    ]

    def __call__(self, args):
        swap = args.swap
        advance = args.advance
        interval = args.interval

        try:
            if swap:
                if advance or interval:
                    message = "Error: Invalid arguments for swap monitoring"
                    MemoryUsageResponse.error(message=message)
                else:
                    swap = psutil.swap_memory()
                    data = {'swap': swap}
                    MemoryUsageResponse.success(data=data)
                    sys.exit(0)
            else:
                if interval and interval < 0:
                    message = "Error: Interval must be a positive integer!"
                    MemoryUsageResponse.error(message=message)

                while True:
                    memory = psutil.virtual_memory()
                    data = {'memory':memory, 'advance':advance}
                    MemoryUsageResponse.success(data=data)

                    if not interval:
                        sys.exit(0)
                    else:
                        time.sleep(interval)
        except KeyboardInterrupt:
            message = " Monitoring Stoped"
            MemoryUsageResponse.error(message=message)
            sys.exit(0)

        except Exception as e:
            MemoryUsageResponse.error(message=e)
            sys.exit(0)
