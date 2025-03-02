import psutil
import time

from utilities.dataFetcher.dataFetcher import DataFetcher


class NetworkIODataFetcher(DataFetcher):

    @staticmethod
    def fetch(args):
        pernic = args.pernic
        network_io = psutil.net_io_counters(pernic=pernic) # getting network I/O , per network argument hndling inline
        return {'network_io': network_io, 'pernic': pernic}


class ActiveConnectionDataFetcher(DataFetcher):

    @staticmethod
    def fetch(args):
        network_connections = psutil.net_connections(kind="inet") # getting network active connections (TCP | UDP)
        return {'network_connections':network_connections}


class NetworkProcessDataFetcher(DataFetcher):

    @staticmethod
    def fetch(args):
        processes = []
        network_connections = psutil.net_connections(kind="inet") # getting network active connections
        for conn in network_connections: 
            if conn.pid: # check if connections has process
                connection_process = psutil.Process(conn.pid) # getting process based on pid
                if connection_process:
                    processes.append({'connection':conn, 'connection_process': connection_process})
        
        return processes


class NetworkSpeedDataFetcher(DataFetcher):

    @staticmethod
    def fetch(args):

        old_stats =  psutil.net_io_counters() # get current network I/O
        time.sleep(1)
        new_stats = psutil.net_io_counters() # get network I/O after 1s

        # calculate upload and download speed
        upload_speed = (new_stats.bytes_sent - old_stats.bytes_sent) / 1024
        download_speed = (new_stats.bytes_recv - old_stats.bytes_recv) / 1024

        return {'upload_speed': upload_speed, 'download_speed': download_speed}
