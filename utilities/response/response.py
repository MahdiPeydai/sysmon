import sys

from abc import ABC, abstractmethod


# responce interface for hanldling commands response
class Response(ABC):
    
    # success response for command
    @staticmethod
    @abstractmethod
    def success(data, exit=None):
        pass


    # error response for command
    @staticmethod
    @abstractmethod
    def error(message):
        print(message)
        sys.exit(2)
