from deropy.dvm.functions.Function import Function
from deropy.dvm.Smartcontract import SmartContract


class Scid(Function):
    def __init__(self):
        func_parameters = {
            'value': {"type": "int", "value": None},
        }
        super().__init__("scid", 2000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        value = SmartContract.scid
        self.parameters['value']['value'] = value
        return value

    def _computeGasStorageCost(self):
        return 0


def scid():
    return Scid()()
