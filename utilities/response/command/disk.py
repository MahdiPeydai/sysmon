from utilities.response.response import Response


# cpu usage command response handler
class DiskUsageResponse(Response):
    
    # disk usage command handler
    @staticmethod
    def success(data):
        if 'input_output' in data:
            if 'per_disk' in data and data['per_disk']:
                for disk, disk_io in data['input_output'].items():
                    print(disk)
                    print(f"Read : {disk_io.read_bytes / 1e+6:.2f} MB, Write : {disk_io.write_bytes / 1e+6:.2f} MB")
            else:
                disk_io = data['input_output']
                print(f"Read : {disk_io.read_bytes / 1e+6:.2f} MB, Write : {disk_io.write_bytes / 1e+6:.2f} MB")
        else:
            disk_usage = data['disk_usage']
            device = data['device']
            print(device)
            print(f"Read : {disk_usage.total / 1e+9:.2f} GB, Used : {disk_usage.used / 1e+9:.2f} GB, Free : {disk_usage.free / 1e+9:.2f} GB")

