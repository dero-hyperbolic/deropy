from deropy.dvm.functions.Function import Function

class Load(Function):
    def __init__(self):
        func_parameters = {
            "key": {"type": "str", "value": None},
        }
        super().__init__("load", 5000, 0, func_parameters)

    def _computeGasStorageCost(self):
        if isinstance(self.parameters["key"]["value"], int):
            return 1
        else:
            size = len(self.parameters["key"]["value"])
            if size < 10: return 1
            return size // 10

    def _exec(self, *args, **kwargs):
        self.parameters["key"]["value"] = kwargs["key"]
        return self.sc.storage[kwargs["key"]]
    
def load(key: str):
    return Load()(key=key)

def load_dero(key: str):
    l =  Load()
    l(key=key)
    return l.convert()