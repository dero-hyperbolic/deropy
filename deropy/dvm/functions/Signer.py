from deropy.dvm.functions.Function import Function
from deropy.dvm.dvm import Dvm

class Signer(Function):
    def __init__(self):
        func_parameters = {}
        super().__init__("signer", 5_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        return "signer"
    
    def _computeGasStorageCost(self):
        return 0
    
    def convert(self):
        return "SIGNER()"

    def __str__(self):
        return self.convert()

def signer():
    return Signer()()

def signer_dero():
    s =  Signer()
    s()
    return s.convert()