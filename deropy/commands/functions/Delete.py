import logging

from deropy.dvm.functions.Function import Function
from deropy.dvm.sc import SmartContract

class Delete(Function):
    def __init__(self):
        func_parameters = {
            'key': {"type": "str", "value": None},
        }
        super().__init__("delete", 50_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters['key']['value'] = kwargs['key']
        return kwargs['key'] in self.sc.storage
    
    def _computeGasStorageCost(self):
        return 0
    
    def convert(self, *args, **kwargs):
        return f'DELETE("{self.parameters["key"]["value"]}")'
        
    def __str__(self):
        return f'DELETE("{self.parameters["key"]["value"]}")'
            
        
def delete(key: str):
    return Delete()(key=key)

def delete_dero(key: str):
    e =  Delete()
    e(key=key)
    return e.convert(key=key)