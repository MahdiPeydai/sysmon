import psutil
import time
import sys

from easycli import SubCommand, Argument, Mutex

from utilities.response.command.network import NetworkUsageResponse


class Network(SubCommand):
    __command__ = 'network'
    __arguments__ = [
        # argument for monitoring in intervals
        Argument(
            '-i', '--interval',
            action='store',
            type=float,
            help='Interval in seconds'
        ),
        # argument for monitoring 
        Argument(
            '-pn', '--per-nic',
            action="store_true",
            help='I/O per Network Interface'
        ),
        # defining mutex arguments
        Mutex(
            # argument for monitoring upload and download speed
            Argument(
                '-s', '--speed',
                action='store_true',
                help='Speed in real-time'
            ),
            # argument for monitoring active connections of system
            Argument(
                '-c', '--connection',
                action="store_true",
                help='Active Connections'
            ),
            # argument for monitoring processes working with network 
             Argument(
                '-p', '--process',
                action="store_true",
                help='Processes Using Network'
            )
        )
    ]

    def __call__(self, args):
        per_nic = args.per_nic
        speed = args.speed
        process = args.process
        active_connection = args.connection
        interval = args.interval
        if interval and interval < 0: # validating interval argument
            message = "Error: Interval must be a positive integer!"
            MemoryUsageResponse.error(message=message, code=2)

        try:
            if active_connection: # handling active connections monitoring
                if interval or per_nic: # handling addition arguments
                    message = 'Invalid Arguments : monitoring active connections do not accept any arguments'
                    NetworkUsageResponse.error(message=message, code=2)

                network_connections = psutil.net_connections(kind="inet") # getting network active connections (TCP | UDP)
                data = {'active_connection': active_connection, 'network_connections':network_connections} # composing data for response
                NetworkUsageResponse.success(data=data) # calling response class success method
                 
            elif process: # handling network processes monitoring
                if interval or per_nic: # handling addition arguments
                    message = 'Invalid Arguments : monitoring process do not accept any arguments'
                    NetworkUsageResponse.error(message=message, code=2)

                network_connections = psutil.net_connections(kind="inet") # getting network active connections
                for conn in network_connections: 
                    if conn.pid: # check if connections has process
                        connection_process = psutil.Process(conn.pid) # getting process based on pid
                        if connection_process:
                            data = {'network_process': process, 'connection':conn, 'connection_process': connection_process}
                            NetworkUsageResponse.success(data=data)
            elif speed: # handling network speed monitoring
                if per_nic: # handling addition arguments
                    message = 'Invalid Arguments : monitoring process do not accept --per-nic argument'
                    NetworkUsageResponse.error(message=message, code=2)

                old_stats =  psutil.net_io_counters() # get current network I/O
                while True: # handling interval
                    time.sleep(1)
                    new_stats = psutil.net_io_counters() # get network I/O after 1s

                    # calculate upload and download speed
                    upload_speed = (new_stats.bytes_sent - old_stats.bytes_sent) / 1024
                    download_speed = (new_stats.bytes_recv - old_stats.bytes_recv) / 1024

                    data = {'network_speed': speed, 'upload_speed': upload_speed, 'download_speed': download_speed}
                    NetworkUsageResponse.success(data=data)

                    if not interval:
                        sys.exit(0)
                    else:
                        time.sleep(interval-1)
                        old_stats = new_stats
            else: # handling network I/O monitoring
                while True: # handling interval
                    network_input_output = psutil.net_io_counters(pernic=per_nic) # getting network I/O , per network argument hndling inline
                    data = {'network_input_output': network_input_output, 'per_nic': per_nic}
                    NetworkUsageResponse.success(data=data)

                    if not interval:
                        sys.exit(0)
                    else:
                        time.sleep(interval)
    
        # handling user privileges error
        except psutil.AccessDenied:
            message = " Root privileges required"
            NetworkUsageResponse.error(message=message)
            sys.exit(0)


        except KeyboardInterrupt:
            message = ""
            NetworkUsageResponse.error(message=message, code=0)

        except Exception as e:
            NetworkUsageResponse.error(message=e, code=2)
