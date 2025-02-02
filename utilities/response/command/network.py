from utilities.response.response import Response


# network usage command response handler
class NetworkUsageResponse(Response):
    
    # network usage command handler
    @staticmethod
    def success(data):
        if 'network_process' in data and 'connection' in data and 'connection_process' in data:
            process = data['connection_process']
            connection = data['connection']
            local_ip, local_port = connection.laddr
            remote_ip, remote_port = connection.raddr if connection.raddr else ("-", "-")
            print(f"Process: {process.name()} (PID: {connection.pid})")
            print(f"Local: {local_ip}:{local_port} → Remote: {remote_ip}:{remote_port}")
            print(f"Status: {connection.status}\n")
        
        elif 'active_connection' in data and 'network_connections' in data:
            connections = data['network_connections']
            for connection in connections:
                print(f"Local: {connection.laddr}, Remote: {connection.raddr}, Status: {connection.status}")

        elif 'network_speed' in data and 'upload_speed' in data and 'download_speed' in data:
            print(f"Upload: {data['upload_speed']:.2f} KB/s, Download: {data['download_speed']:.2f} KB/s")
        
        else:
            if 'per_nic' in data and data['per_nic']:
                for network, network_io in data['network_input_output'].items():
                    print(network)
                    print(f"Bytes Sent : {network_io.bytes_sent / (1024 ** 2):.2f} MB, Bytes Received : {network_io.bytes_recv / (1024 ** 2):.2f} MB")
            else:
                network_io = data['network_input_output']
                print(f"Bytes Sent : {network_io.bytes_sent / (1024 ** 2):.2f} MB, Bytes Received : {network_io.bytes_recv / (1024 ** 2):.2f} MB")

