import logging

from deropy.dvm.functions.Function import Function
from deropy.dvm.sc import SmartContract

class Return(Function):
    def __init__(self):
        func_parameters = {
            'value': {"type": "int", "value": None},
        }
        super().__init__("return", 50_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters['value']['value'] = kwargs['value']

    def _computeGasStorageCost(self):
        return 0

    def convert(self, *args, **kwargs):
        return f'RETURN {self.parameters["value"]["value"]}'
        
    def __str__(self):
        return f'RETURN {self.parameters["value"]["value"]}'
            
        
def ret(value: str):
    return Return()(value=value)

def ret_dero(value: str):
    r =  Return()
    r(value=value)
    return r.convert(value=value)