from easycli import SubCommand, Argument, Mutex

from utilities.response.commands.network import NetworkIOResponseHandler, ActiveConnectionResponseHandler, NetworkProcessResponseHandler, NetworkSpeedResponseHandler
from utilities.dataFetcher.commands.network import NetworkIODataFetcher, ActiveConnectionDataFetcher, NetworkProcessDataFetcher, NetworkSpeedDataFetcher
from utilities.monitoring.monitoring import Monitoring


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
        # argument for monitoring I/O per network interface
        Argument(
            '-p', '--pernic',
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
                '--ps',
                action="store_true",
                help='Processes Using Network'
            )
        )
    ]

    def __call__(self, args):
        pernic = args.pernic
        speed = args.speed
        process = args.ps
        active_connection = args.connection
        interval = args.interval

        if active_connection: # handling active connections monitoring
            if interval or pernic: # handling addition arguments
                message = 'Disallowed Arguments : monitoring active connections do not accept any arguments'
                NetworkIOResponseHandler.error(message=message)

            activeConnection_monitor = Monitoring(data_fetcher=ActiveConnectionDataFetcher, response_handler=ActiveConnectionResponseHandler)
            activeConnection_monitor.monitor(args)

        elif process: # handling network processes monitoring
            if interval or pernic: # handling addition arguments
                message = 'Disallowed Arguments : monitoring network processes do not accept any arguments'
                NetworkIOResponseHandler.error(message=message)

            network_process_monitor = Monitoring(data_fetcher=NetworkProcessDataFetcher, response_handler=NetworkProcessResponseHandler)
            network_process_monitor.monitor(args)
        
        elif speed: # handling network speed monitoring
            if pernic: # handling addition arguments
                message = 'Disallowed Arguments : monitoring network speed do not accept --pernic argument'
                NetworkIOResponseHandler.error(message=message)

            network_speed_monitor = Monitoring(data_fetcher=NetworkSpeedDataFetcher, response_handler=NetworkSpeedResponseHandler)
            network_speed_monitor.monitor(args)

        else: # handling network I/O monitoring
            network_io_monitor = Monitoring(data_fetcher=NetworkIODataFetcher, response_handler=NetworkIOResponseHandler)
            network_io_monitor.monitor(args)

