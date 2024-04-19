from deropy.dvm.functions.Function import Function

class SendAssetToAddress(Function):
    def __init__(self):
        func_parameters = {
            "raw_address": {"type": "str", "value": None},
            "amount": {"type": "int", "value": None},
            "asset": {"type": "str", "value": None},
        }
        super().__init__("send_asset_to_address", 70_000, 0, func_parameters)

    def _computeGasStorageCost(self):
        return len(self.parameters["raw_address"]["value"]) + len(self.parameters["asset"]["value"])

    def _exec(self, *args, **kwargs):
        self.parameters["raw_address"]["value"] = kwargs["raw_address"]
        self.parameters["amount"]["value"] = kwargs["amount"]
        self.parameters["asset"]["value"] = kwargs["asset"]
        return 0
    
def send_asset_to_address(raw_address: str, amount: int, asset: str):
    return SendAssetToAddress()(raw_address=raw_address, amount=amount, asset=asset)
