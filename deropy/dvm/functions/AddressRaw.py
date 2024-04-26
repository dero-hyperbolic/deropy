from deropy.dvm.functions.Function import Function

class AddressRaw(Function):
    def __init__(self):
        func_parameters = {
            "address": {"type": "str", "value": None},
        }
        super().__init__("address_raw", 60_000, 0, func_parameters)

    def _computeGasStorageCost(self):
        return 0

    def _exec(self, *args, **kwargs):
        self.parameters["address"]["value"] = kwargs["address"]\
        
        return kwargs["address"][:33]  # raw address is 33 bytes long
    
def address_raw(address: str):
    return AddressRaw()(address=address)
