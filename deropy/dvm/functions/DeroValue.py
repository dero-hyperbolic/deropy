from deropy.dvm.functions.Function import Function


class DeroValue(Function):
    def __init__(self):
        func_parameters = {}
        super().__init__("dero_value", 10_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        return self.sc.dero_value
    
    def _computeGasStorageCost(self): 
        return 0

def dero_value():
    return DeroValue()()