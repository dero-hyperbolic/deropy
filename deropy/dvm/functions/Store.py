from deropy.dvm.functions.Function import Function
from deropy.dvm.dvm import Dvm

class Store(Function):
    def __init__(self):
        func_parameters = {
            "key": {"type": "str", "value": None},
            "value": {"type": "Any", "value": None},
        }
        super().__init__("store", 10_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["key"]["value"] = kwargs["key"]
        self.parameters["value"]["value"] = kwargs["value"]
        self.sc.storage[kwargs["key"]] = kwargs["value"]

    def _computeGasStorageCost(self):
        if isinstance(self.parameters["key"]["value"], int):
            return 8
        else:
            return len(self.parameters["key"]["value"])

    def convert(self):
        if type(self.parameters["value"]["value"]) == str:
            return f'STORE({self.parameters["key"]["value"]}, {self.parameters["value"]["value"]})'
        elif type(self.parameters["value"]["value"]) == int:
            return f'STORE({self.parameters["key"]["value"]}, {self.parameters["value"]["value"]})'
        else:
            raise Exception(f'Invalid type {type(self.parameters["value"]["value"])} for argument value provided to function store')
        
    def __str__(self):
        return self.convert()

def store(variable: str, value):
    return Store()(key=variable, value=value)

def store_dero(variable: str, value):
    s =  Store()
    s(key=variable, value=value)
    return s.convert()