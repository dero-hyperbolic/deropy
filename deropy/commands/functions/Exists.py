import logging

from deropy.dvm.functions.Function import Function
from deropy.dvm.sc import SmartContract

class Exists(Function):
    def __init__(self):
        func_parameters = {
            'key': {"type": "str", "value": None},
        }
        super().__init__("exists", 50_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters['key']['value'] = kwargs['key']
        return kwargs['key'] in self.sc.storage
    
    def _computeGasStorageCost(self):
        return 0
    
    def convert(self, *args, **kwargs):
        return f'EXISTS("{self.parameters["key"]["value"]}")'
        
    def __str__(self):
        return f'EXISTS("{self.parameters["key"]["value"]}")'
            
        
def exists(key: str):
    return Exists()(key=key)

def exists_dero(key: str):
    e =  Exists()
    e(key=key)
    return e.convert(key=key)