from deropy.dvm.functions.Function import Function
from deropy.dvm.dvm import Dvm

class MapStore(Function):
    def __init__(self):
        func_parameters = {
            "key": {"type": "str", "value": None},
            "value": {"type": "Any", "value": None},
        }
        super().__init__("mapstore", 1000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["key"]["value"] = kwargs["key"]
        self.parameters["value"]["value"] = kwargs["value"]
        self.sc.storage[kwargs["key"]] = kwargs["value"]

    def _computeGasStorageCost(self):
        return 0

    def convert(self):
        if type(self.parameters["value"]["value"]) == str:
            return f'MAPSTORE({self.parameters["key"]["value"]}, {self.parameters["value"]["value"]})'
        elif type(self.parameters["value"]["value"]) == int:
            return f'MAPSTORE({self.parameters["key"]["value"]}, {self.parameters["value"]["value"]})'
        else:
            raise Exception(f'Invalid type {type(self.parameters["value"]["value"])} for argument value provided to function map store')
        
    def __str__(self):
        return self.convert()

def map_store(variable: str, value):
    return MapStore()(key=variable, value=value)

def map_store_dero(variable: str, value):
    s =  MapStore()
    s(key=variable, value=value)
    return s.convert()