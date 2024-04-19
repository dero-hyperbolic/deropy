from deropy.dvm.functions.Function import Function

class AddressString(Function):
    def __init__(self):
        func_parameters = {
            "address": {"type": "str", "value": None},
        }
        super().__init__("address_string", 60_000, 0, func_parameters)

    def _computeGasStorageCost(self):
        return len(self.parameters["address"]["value"])

    def _exec(self, *args, **kwargs):
        self.parameters["address"]["value"] = kwargs["address"]
        return kwargs["address"]  # FIXME: This is a placeholder value
    
def address_string(address: str):
    return AddressString()(address=address)
