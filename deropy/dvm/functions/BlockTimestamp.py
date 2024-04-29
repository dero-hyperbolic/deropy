import datetime

from deropy.dvm.functions.Function import Function


class BlockTimestamp(Function):
    def __init__(self):
        func_parameters = {}
        super().__init__("block_timestamp", 2500, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        block_height = int(datetime.datetime.now().timestamp()) % 18
        return block_height

    def _computeGasStorageCost(self):
        return 0


def block_timestamp():
    return BlockTimestamp()()
