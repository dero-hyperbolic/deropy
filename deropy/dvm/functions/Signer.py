from deropy.dvm.functions.Function import Function
from deropy.dvm.Smartcontract import SmartContract


class Signer(Function):
    def __init__(self):
        func_parameters = {}
        super().__init__("signer", 5_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        return SmartContract.active_wallet[:33]
    
    def _computeGasStorageCost(self):
        return 0

def signer():
    return Signer()()