import psutil
import time
import sys

from easycli import SubCommand, Argument

from utilities.response.command.disk import DiskUsageResponse


class Disk(SubCommand):
    __command__ = 'disk'
    __arguments__ = [
        Argument(
            '-i', '--interval',
            action='store',
            type=float,
            help='Interval in seconds'
        ),
        Argument(
            '-io', '--input-output',
            action='store_true',
            help='Disk I/O'
        ),
        Argument(
            '-pd', '--per-disk',
            action="store_true",
            help='I/O per disk'
        )
    ]

    def __call__(self, args):
        interval = args.interval
        per_disk = args.per_disk
        input_output = args.input_output

        try:
            if input_output:
                while True:
                    disk_input_output = psutil.disk_io_counters(perdisk=per_disk)
                    data = {'input_output': disk_input_output, 'per_disk': per_disk}
                    DiskUsageResponse.success(data=data)

                    if not interval:
                        sys.exit(0)
                    else:
                        time.sleep(interval)
            else:
                if per_disk:
                    message = 'Invalid Argument : --per-disk'
                    DiskUsageResponse.error(message=message)


                while True:
                    system_disks = psutil.disk_partitions()
                    for disk in system_disks: 
                        disk_usage = psutil.disk_usage(disk.mountpoint)
                        data = {'disk_usage': disk_usage, 'device':disk.device}
                        DiskUsageResponse.success(data=data)
                    if not interval:
                        sys.exit(0)
                    else:
                        time.sleep(interval)

        except KeyboardInterrupt:
            message = " Monitoring Stoped"
            DiskUsageResponse.error(message=message)
            sys.exit(0)

        except Exception as e:
            DiskUsageResponse.error(message=e)
            sys.exit(0)
