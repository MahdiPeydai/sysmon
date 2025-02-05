import psutil
import time
import sys

from easycli import SubCommand, Argument, Mutex

from utilities.response.command.memory import MemoryUsageResponse


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
        advance = args.advance
        interval = args.interval
        if interval and interval < 0: # validating interval argument
            message = "Error: Interval must be a positive integer!"
            MemoryUsageResponse.error(message=message, code=2)

        try:
            if swap: # handling swap usage monitoring
                while True: # handling interval
                    swap = psutil.swap_memory() # getting swap memory
                    data = {'swap': swap} # composing data for response
                    MemoryUsageResponse.success(data=data) # calling response class success method

                    if not interval:
                        sys.exit(0)
                    else:
                        time.sleep(interval)

            else: # handling memory usage monitoring
                while True:
                    memory = psutil.virtual_memory() # geeting memory usage
                    data = {'memory':memory, 'advance':advance} # handling advance argument
                    MemoryUsageResponse.success(data=data)

                    if not interval:
                        sys.exit(0)
                    else:
                        time.sleep(interval)

        except KeyboardInterrupt: 
            message = ''
            CpuUsageResponse.error(message=message, code=0) # calling response class error method

        except Exception as e:
            CpuUsageResponse.error(message=e)
