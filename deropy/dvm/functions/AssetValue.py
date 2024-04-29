from deropy.dvm.functions.Function import Function
from deropy.dvm.Smartcontract import SmartContract


class AssetValue(Function):
    def __init__(self):
        func_parameters = {
            "asset": {"type": "str", "value": None},
        }
        super().__init__("asset_value", 10_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        asset_id = kwargs["asset"]

        if SmartContract.asset_value is None:
            return 0
        if asset_id not in SmartContract.asset_value:
            return 0

        self.parameters["asset"]["value"] = asset_id
        return SmartContract.asset_value[asset_id]

    def _computeGasStorageCost(self):
        return 0


def asset_value(asset: str):
    return AssetValue()(asset=asset)
