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
            
        
def delete(key: str):
    return Delete()(key=key)