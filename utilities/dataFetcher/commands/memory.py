import psutil

from utilities.dataFetcher.dataFetcher import DataFetcher


class MemoryDataFetcher(DataFetcher):

    @staticmethod
    def fetch(args):
        advance = args.advance
        memory = psutil.virtual_memory() # geeting memory usage

        return {'memory':memory, 'advance':advance}


class SwapDataFetcher(DataFetcher):

    @staticmethod
    def fetch(args):
        swap = psutil.swap_memory() # getting swap memory
        
        return {'swap': swap}
