import psutil
import time
import sys

from easycli import SubCommand, Argument

from utilities.response.command.cpu import CpuUsageResponse


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
            '-pc', '--per-core',
            action='store_true',
            help='Cpu usage per core'
        )
    ]

    def __call__(self, args):
        per_core = args.per_core
        interval = args.interval
        if interval and interval < 0: # validating interval argument
            message = "Error: Interval must be a positive integer!"
            MemoryUsageResponse.error(message=message, code=2)
        
        try:
            while True: # handling interval
                cpu_usage = psutil.cpu_percent(interval=interval, percpu=per_core) # handle per core argument inline
                data = {"cpu_usage": cpu_usage, "per_core": per_core} # composing data for response
                CpuUsageResponse.success(data=data) # calling response class success method

                if not interval:
                    sys.exit(0)
                else:
                    time.sleep(interval)

        except KeyboardInterrupt: # kill signal (ctrl+C) handling
            message = ''
            CpuUsageResponse.error(message=message, code=0) # calling response class error method

        except Exception as e:
            CpuUsageResponse.error(message=e)
