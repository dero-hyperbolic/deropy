from deropy.dvm.functions.Function import Function
import sha3


class Keccak256(Function):
    def __init__(self):
        func_parameters = {
            "s": {"type": "str", "value": None},
        }
        super().__init__("keccak256", 25_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["s"]["value"] = kwargs["s"]
        return sha3.keccak_256().update(kwargs["s"].encode()).hexdigest()
    
    def _computeGasStorageCost(self): 
        return 0

def keccak256(s: str):
    return Keccak256()(s=s)