from deropy.dvm.functions.Function import Function


class Load(Function):
    def __init__(self):
        func_parameters = {
            "key": {"type": "str", "value": None},
        }
        super().__init__("load", 5000, 0, func_parameters)

    def _computeGasStorageCost(self):
        if self.sc.storage[self.parameters["key"]["value"]] is None:
            raise Exception(f"KeyError: {self.parameters['key']['value']} not found in SmartContract storage")

        loaded_value = self.sc.storage[self.parameters["key"]["value"]]
        if isinstance(loaded_value, int):
            return 1

        if len(loaded_value) < 10:
            return 1
        return len(loaded_value) // 10

    def _exec(self, *args, **kwargs):
        self.parameters["key"]["value"] = kwargs["key"]
        return self.sc.load(kwargs["key"])


def load(key: str):
    return Load()(key=key)
