from utilities.response.response import Response


# cpu usage command response handler
class CpuResponseHandler(Response):
    
    # cpu usage command handler
    @staticmethod
    def success(data):
        cpu_usage = data['cpu_usage']

        # argumnet -pc for showing usage for per core
        if data['percore']:
            for i, usage in enumerate(cpu_usage):
                print(f"Core {i + 1} usage : {usage}%")

        # pure command for showing system cpu usage
        else:
            print(f"CPU Usage : {cpu_usage}%")
