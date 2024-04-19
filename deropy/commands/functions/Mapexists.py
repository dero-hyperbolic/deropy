import logging

from deropy.dvm.functions.Function import Function
from deropy.dvm.sc import SmartContract

class MapExists(Function):
    def __init__(self):
        func_parameters = {
            'key': {"type": "str", "value": None},
        }
        super().__init__("mapexist", 1000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters['key']['value'] = kwargs['key']
        return kwargs['key'] in self.sc.storage
    
    def _computeGasStorageCost(self):
        return 0
    
    def convert(self, *args, **kwargs):
        return f'MAPEXISTS("{self.parameters["key"]["value"]}")'
        
    def __str__(self):
        return f'MAPEXISTS("{self.parameters["key"]["value"]}")'
            
        
def map_exists(key: str):
    return MapExists()(key=key)

def map_exists_dero(key: str):
    e =  MapExists()
    e(key=key)
    return e.convert(key=key)