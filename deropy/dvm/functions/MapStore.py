from deropy.dvm.functions.Function import Function


class MapStore(Function):
    def __init__(self):
        func_parameters = {
            "key": {"type": "str", "value": None},
            "value": {"type": "Any", "value": None},
        }
        super().__init__("mapstore", 1000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["key"]["value"] = kwargs["key"]
        self.parameters["value"]["value"] = kwargs["value"]
        self.sc.memory[kwargs["key"]] = kwargs["value"]

    def _computeGasStorageCost(self):
        return 0


def map_store(variable: str, value):
    return MapStore()(key=variable, value=value)
