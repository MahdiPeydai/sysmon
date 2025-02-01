from utilities.response.response import Response


# cpu usage command response handler
class CpuUsageResponse(Response):
    
    # cpu usage command handler
    @staticmethod
    def success(data):
        cpu_usage = data['cpu_usage']

        if data['per_core']:
            for i, usage in enumerate(cpu_usage):
                print(f"Core {i} : {usage}%")
        else:
            print(f"CPU Usage : {cpu_usage}%")
