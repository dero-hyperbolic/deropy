import datetime

from deropy.dvm.functions.Function import Function


class BlockHeight(Function):
    def __init__(self):
        func_parameters = {}
        super().__init__("block_height", 2000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        mainnet_start_timestamp = 1648774702
        block_height = (int(datetime.datetime.now().timestamp()) - mainnet_start_timestamp) / 18
        return block_height

    def _computeGasStorageCost(self):
        return 0


def block_height():
    return BlockHeight()()
