import psutil
import time
import sys

from easycli import SubCommand, Argument

from utilities.response.command.cpu import CpuUsageResponse


class Cpu(SubCommand):
    __command__ = 'cpu'
    __arguments__ = [
        Argument(
            '-i', '--interval',
            action='store',
            type=float,
            help='Interval in seconds'
        ),
        Argument(
            '-pc', '--per-core',
            action='store_true',
            help='Cpu usage per core'
        )
    ]

    def __call__(self, args):
        interval = args.interval
        per_core = args.per_core

        try:
            while True:
                cpu_usage = psutil.cpu_percent(interval=interval, percpu=per_core)
                data = {"cpu_usage": cpu_usage, "per_core": per_core}
                CpuUsageResponse.success(data=data)

                if not interval:
                    sys.exit(0)
                else:
                    time.sleep(interval)

        except KeyboardInterrupt:
            message = " Monitoring Stoped"
            CpuUsageResponse.error(message=message)
            sys.exit(0)

        except Exception as e:
            CpuUsageResponse.error(message=e)
            sys.exit(0)
