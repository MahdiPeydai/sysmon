from abc import ABC, abstractmethod


class DataFetcher(ABC):

    @staticmethod
    @abstractmethod
    def fetch(args):
        pass
