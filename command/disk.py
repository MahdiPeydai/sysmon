import psutil
import time
import sys

from easycli import SubCommand, Argument

from utilities.response.command.disk import DiskUsageResponse


# Disk usage monitoring command
class Disk(SubCommand):
    __command__ = 'disk'
    __arguments__ = [
        # argument for monitoring usage in intervals
        Argument(
            '-i', '--interval',
            action='store',
            type=float,
            help='Interval in seconds'
        ),
        # argument for monitoring disk I/O
        Argument(
            '-io', '--input-output',
            action='store_true',
            help='Disk I/O'
        ),
        # argument for monitoring I/O per disk
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
        if interval and interval < 0: # validating interval argument
            message = "Error: Interval must be a positive integer!"
            MemoryUsageResponse.error(message=message, code=2)

        try:
            if input_output: # handling monitoring I/O
                while True: # handling interval
                    disk_input_output = psutil.disk_io_counters(perdisk=per_disk) # handling per disk argument inline
                    data = {'disk_input_output': disk_input_output, 'per_disk': per_disk} # composing data for response
                    DiskUsageResponse.success(data=data) # calling response class success method

                    if not interval:
                        sys.exit(0)
                    else:
                        time.sleep(interval)
            
            elif per_disk and not input_output: # handling per disk argument to just work with io argument
                message = 'Invalid Argument : --per-disk'
                DiskUsageResponse.error(message=message, code=2)

            else:
                while True:
                    system_disks = psutil.disk_partitions() # getting system disks
                    for disk in system_disks: # getting usage for every disk
                        disk_usage = psutil.disk_usage(disk.mountpoint) # getting disk usage
                        data = {'disk_usage': disk_usage, 'device':disk.device}
                        DiskUsageResponse.success(data=data)
                    
                    if not interval:
                        sys.exit(0)
                    else:
                        time.sleep(interval)

        except KeyboardInterrupt: # kill signal (ctrl+C) handling
            message = ''
            CpuUsageResponse.error(message=message, code=0) # calling response class error method

        except Exception as e:
            CpuUsageResponse.error(message=e)
