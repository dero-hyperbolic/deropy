from deropy.dvm.functions.Function import Function


class MapGet(Function):
    def __init__(self):
        func_parameters = {
            "key": {"type": "str", "value": None},
        }
        super().__init__("mapget", 1000, 0, func_parameters)

    def _computeGasStorageCost(self):
        return 0

    def _exec(self, *args, **kwargs):
        self.parameters["key"]["value"] = kwargs["key"]
        return self.sc.memory[kwargs["key"]]


def map_get(key: str):
    return MapGet()(key=key)
