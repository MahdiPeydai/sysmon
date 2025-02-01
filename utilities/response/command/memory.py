import platform

from utilities.response.response import Response


class MemoryUsageResponse(Response):

    @staticmethod
    def success(data):
        if 'swap' in data:
            swap = data['swap']
            print("Swap")
            print(f"Total: {swap.total / 1e+9:.2f}GB")
            print(f"Used: {swap.used / 1e+9:.2f}GB / {swap.percent}%")
            print(f"Free: {swap.free / 1e+9:.2f}GB")
        else:
            memory = data['memory']
            if data['advance']:
                print(f"Total: {memory.total / 1e+9:.2f} GB")
                print(f"Available: {memory.available / 1e+9:.2f} GB")
                print(f"Used: {memory.used / 1e+9:.2f} GB / {memory.percent}%")
                print(f"Free: {memory.free / 1e+9:.2f} GB")
                if platform.system() == "Linux":
                    print(f"Shared: {memory.shared / 1e+9:.2f} GB")
                    print(f"Cache: {memory.cached / 1e+9:.2f} GB")
                    print(f"buffered: {memory.buffers / 1e+9:.2f} GB")
            else:
                print(f"Total: {memory.total / 1e+9:.2f}GB  Used: {memory.used / 1e+9:.2f}GB  Free: {memory.available / 1e+9:.2f}GB")
