import logging
import random as rd

from deropy.dvm.functions.Function import Function


class Scid(Function):
    def __init__(self):
        func_parameters = {
            'value': {"type": "int", "value": None},
        }
        super().__init__("scid", 2000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        value = "f62fa283bf76fe0da393218ce84737c78988b539f79bf8316acaffb806d108bc" # FIXME: Find a way to get this value from the singleton
        self.parameters['value']['value'] = value
        return value
    
    def _computeGasStorageCost(self):
        return 0
            
        
def scid():
    return Scid()()
