from deropy.dvm.functions.Function import Function


class SendDeroToAddress(Function):
    def __init__(self):
        func_parameters = {
            "raw_address": {"type": "str", "value": None},
            "amount": {"type": "int", "value": None},
        }
        super().__init__("send_dero_to_address", 70_000, 0, func_parameters)

    def _computeGasStorageCost(self):
        return len(self.parameters["raw_address"]["value"])

    def _exec(self, *args, **kwargs):
        self.parameters["raw_address"]["value"] = kwargs["raw_address"]
        self.parameters["amount"]["value"] = kwargs["amount"]
        return 0


def send_dero_to_address(raw_address: str, amount: int):
    return SendDeroToAddress()(raw_address=raw_address, amount=amount)
