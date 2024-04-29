from deropy.dvm.functions.Function import Function


class AssetValue(Function):
    def __init__(self):
        func_parameters = {
            "asset": {"type": "str", "value": None},
        }
        super().__init__("asset_value", 10_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["asset"]["value"] = kwargs["asset"]
        return self.sc.asset_value[kwargs["asset"]]
        return 0
        
    def _computeGasStorageCost(self): 
        return 0

def asset_value(asset: str):
    return AssetValue()(asset=asset)