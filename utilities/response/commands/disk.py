from utilities.response.response import Response


# disk usage command response handler
class DiskResponseHandler(Response):
    
    # disk usage command handler
    @staticmethod
    def success(data):
        for disk in data['disks']:
            disk_usage = disk['disk_usage']
            device = disk['device']
            print(device)
            print(f"Total: {disk_usage.total / 1e+9:.2f}GB, Used: {disk_usage.used / 1e+9:.2f}GB, Free: {disk_usage.free / 1e+9:.2f}GB")


# disk I/O command response handler
class DiskIOResponseHandler(Response):
    
    # disk usage command handler
    @staticmethod
    def success(data):
        if 'perdisk' in data and data['perdisk']:
            for disk, disk_io in data['disk_io'].items():
                print(disk)
                print(f"Read: {disk_io.read_bytes / 1e+6:.2f}MB, Write: {disk_io.write_bytes / 1e+6:.2f}MB")
        else:
            disk_io = data['disk_io']
            print(f"Read: {disk_io.read_bytes / 1e+6:.2f}MB, Write: {disk_io.write_bytes / 1e+6:.2f}MB")
