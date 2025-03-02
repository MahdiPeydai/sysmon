import psutil

from utilities.dataFetcher.dataFetcher import DataFetcher


class CpuDataFetcher(DataFetcher):

    @staticmethod
    def fetch(args):
        percore = args.percore
        cpu_usage = psutil.cpu_percent(percpu=percore)

        return {"cpu_usage": cpu_usage, "percore": percore}
