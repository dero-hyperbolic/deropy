from deropy.dvm.functions.Function import Function


class IsAddressValid(Function):
    def __init__(self):
        func_parameters = {
            "address": {"type": "str", "value": None},
        }
        super().__init__("is_address_valid", 50_000, 0, func_parameters)

    def _computeGasStorageCost(self):
        return 0

    def _exec(self, *args, **kwargs):
        self.parameters["address"]["value"] = kwargs["address"]
        is_valid = 0  # FIXME: This is a placeholder value
        return is_valid


def is_address_valid(address: str):
    return IsAddressValid()(address=address)
