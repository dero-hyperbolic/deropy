import logging
import random as rd

from deropy.dvm.functions.Function import Function
from deropy.dvm.sc import SmartContract

class Random(Function):
    def __init__(self):
        func_parameters = {
            'value': {"type": "int", "value": None},
        }
        super().__init__("random", 2500, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        value = rd.randint(0, self.parameters['value']['value'])
        self.parameters['value']['value'] = kwargs['value']
        return value
    
    def _computeGasStorageCost(self):
        return 0
            
        
def random(value: str):
    return Random()(value=value)
