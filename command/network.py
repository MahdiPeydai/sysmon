import psutil
import time
import sys

from easycli import SubCommand, Argument

from utilities.response.command.network import NetworkUsageResponse


class Network(SubCommand):
    __command__ = 'network'
    __arguments__ = [
        Argument(
            '-i', '--interval',
            action='store',
            type=float,
            help='Interval in seconds'
        ),
        Argument(
            '-s', '--speed',
            action='store_true',
            help='Speed in real-time'
        ),
        Argument(
            '-pn', '--per-nic',
            action="store_true",
            help='I/O per Network Interface'
        ),
        Argument(
            '-c', '--connection',
            action="store_true",
            help='Active Connections'
        ),
        Argument(
            '-p', '--process',
            action="store_true",
            help='Processes Using Network'
        )
    ]

    def __call__(self, args):
        interval = args.interval
        per_nic = args.per_nic
        speed = args.speed
        process = args.process
        active_connection = args.connection

        try:
            if active_connection:
                if interval or per_nic or speed:
                    message = 'Invalid Arguments : monitoring active connections do not accept any arguments'
                    NetworkUsageResponse.error(message=message)
                network_connections = psutil.net_connections(kind="inet")
                data = {'active_connection': active_connection, 'network_connections':network_connections}
                NetworkUsageResponse.success(data=data)
                 
            elif process:
                if interval or per_nic or speed:
                    message = 'Invalid Arguments : monitoring process do not accept any arguments'
                    NetworkUsageResponse.error(message=message)

                network_connections = psutil.net_connections(kind="inet")
                for conn in network_connections: 
                    if conn.pid:
                        connection_process = psutil.Process(conn.pid)
                        if connection_process:
                            data = {'network_process': process, 'connection':conn, 'connection_process': connection_process}
                            NetworkUsageResponse.success(data=data)
            elif speed:
                old_stats =  psutil.net_io_counters()
                while True:
                    time.sleep(1)
                    new_stats = psutil.net_io_counters()
                    upload_speed = (new_stats.bytes_sent - old_stats.bytes_sent) / 1024
                    download_speed = (new_stats.bytes_recv - old_stats.bytes_recv) / 1024
                    data = {'network_speed': speed, 'upload_speed': upload_speed, 'download_speed': download_speed}
                    NetworkUsageResponse.success(data=data)

                    if not interval:
                        sys.exit(0)
                    else:
                        time.sleep(interval-1)
                        old_stats = new_stats
            else:
                 while True:
                    network_input_output = psutil.net_io_counters(pernic=per_nic)
                    data = {'network_input_output': network_input_output, 'per_nic': per_nic}
                    NetworkUsageResponse.success(data=data)

                    if not interval:
                        sys.exit(0)
                    else:
                        time.sleep(interval)
    
        except psutil.AccessDenied:
            message = " Root privileges required"
            NetworkUsageResponse.error(message=message)
            sys.exit(0)


        except KeyboardInterrupt:
            message = " Monitoring Stoped"
            NetworkUsageResponse.error(message=message)
            sys.exit(0)

        except Exception as e:
            NetworkUsageResponse.error(message=e)
            sys.exit(0)
