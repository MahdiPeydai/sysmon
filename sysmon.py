import easycli

from command.cpu import Cpu
from command.memory import Memory
from command.disk import Disk
from command.network import Network

__version__ = '0.0.1'


class Sysmon(easycli.Root):
    __help__ = "system monitoring"
    __arguments__ = [
        easycli.Argument(
            '-v', '--version',
            action='store_true',
            help='show version'
        ),
        Cpu,
        Memory,
        Disk,
        Network
    ]

    def __call__(self, args):
        if args.version:
            print(__version__)
            return
        return super().__call__(args)
