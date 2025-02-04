from utilities.response.response import Response


# cpu usage command response handler
class CpuUsageResponse(Response):
    
    # cpu usage command handler
    @staticmethod
    def success(data):
        cpu_usage = data['cpu_usage']

        # argumnet -pc for showing usage for per core
        if data['per_core']:
            for i, usage in enumerate(cpu_usage):
                print(f"Core {i} usage : {usage}%")
        # pure command for showing system cpu usage
        else:
            print(f"CPU Usage : {cpu_usage}%")
