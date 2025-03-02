from utilities.response.response import Response


class NetworkIOResponseHandler(Response):
    
    @staticmethod
    def success(data):
        if 'pernic' in data and data['pernic']:
            for network, network_io in data['network_io'].items():
                print(network)
                print(f"Bytes Sent: {network_io.bytes_sent / (1024 ** 2):.2f}MB, Bytes Received: {network_io.bytes_recv / (1024 ** 2):.2f}MB")
        else:
            network_io = data['network_io']
            print(f"Bytes Sent: {network_io.bytes_sent / (1024 ** 2):.2f}MB, Bytes Received: {network_io.bytes_recv / (1024 ** 2):.2f}MB")



class ActiveConnectionResponseHandler(Response):
    
    @staticmethod
    def success(data):
        connections = data['network_connections']
        for connection in connections:
            print(f"Local: {connection.laddr}, Remote: {connection.raddr}, Status: {connection.status}")


class NetworkProcessResponseHandler(Response):
    
    @staticmethod
    def success(data):
        network_processes = data['processes']
        for network_process in network_processes:
            process = network_process['connection_process']
            connection = network_process['connection']
            local_ip, local_port = connection.laddr
            remote_ip, remote_port = connection.raddr if connection.raddr else ("-", "-")
            print(f"Process: {process.name()} (PID: {connection.pid})")
            print(f"Local: {local_ip}:{local_port} → Remote: {remote_ip}:{remote_port}")
            print(f"Status: {connection.status}\n")


class NetworkSpeedResponseHandler(Response):
    
    @staticmethod
    def success(data):
        upload_speed = data['upload_speed']
        download_speed = data['download_speed']
        print(f"Upload: {upload_speed:.2f}KB/s, Download: {download_speed:.2f}KB/s")

