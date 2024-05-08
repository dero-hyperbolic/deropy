from deropy.dvm.functions.Function import Function


class Store(Function):
    def __init__(self):
        func_parameters = {
            "key": {"type": "str", "value": None},
            "value": {"type": "Any", "value": None},
        }
        super().__init__("store", 10_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["key"]["value"] = kwargs["key"]
        self.parameters["value"]["value"] = kwargs["value"]
        self.sc.store(kwargs["key"], kwargs["value"])

    def _computeGasStorageCost(self):
        if isinstance(self.parameters["value"]["value"], int):
            return 8
        else:
            return len(self.parameters["value"]["value"])


def store(variable: str, value):
    return Store()(key=variable, value=value)
