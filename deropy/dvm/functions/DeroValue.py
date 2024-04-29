from deropy.dvm.functions.Function import Function
from deropy.dvm.Smartcontract import SmartContract


class DeroValue(Function):
    def __init__(self):
        func_parameters = {}
        super().__init__("dero_value", 10_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        if SmartContract.dero_value is None:
            return 0
        if SmartContract.dero_value < 0:
            return 0
        return SmartContract.dero_value

    def _computeGasStorageCost(self):
        return 0


def dero_value():
    return DeroValue()()
