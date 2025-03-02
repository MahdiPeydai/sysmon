import psutil

from utilities.dataFetcher.dataFetcher import DataFetcher


class DiskDataFetcher(DataFetcher):

    @staticmethod
    def fetch(args):
        system_disks = psutil.disk_partitions() # getting system disks
        disks = []
        for disk in system_disks: # getting usage for every disk
            disk_usage = psutil.disk_usage(disk.mountpoint) # getting disk usage
            disks.append({'disk_usage': disk_usage, 'device':disk.device})

        return {'disks': disks}


class DiskIODataFetcher(DataFetcher):

    @staticmethod
    def fetch(args):
        perdisk = args.perdisk
        disk_io = psutil.disk_io_counters(perdisk=perdisk) # getting disk I/O, handling per disk argument inline

        return {'disk_io': disk_io, 'perdisk': perdisk}

