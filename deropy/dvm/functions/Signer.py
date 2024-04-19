from deropy.dvm.functions.Function import Function


class Signer(Function):
    def __init__(self):
        func_parameters = {}
        super().__init__("signer", 5_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        return "signer"
    
    def _computeGasStorageCost(self):
        return 0

def signer():
    return Signer()()