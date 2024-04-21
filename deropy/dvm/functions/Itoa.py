from deropy.dvm.functions.Function import Function


class Itoa(Function):
    def __init__(self):
        func_parameters = {
            "n": {"type": "int", "value": None},
        }
        super().__init__("itoa", 10_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["n"]["value"] = kwargs["n"]
        
        try:
            return int(str(kwargs["n"]))
        except:
            raise ValueError(f"ITPA({kwargs['s']}) failed")
        
    
    def _computeGasStorageCost(self): 
        return 0   # FIXME: Find a way

def itoa(n: str):
    return Itoa()(n=n)