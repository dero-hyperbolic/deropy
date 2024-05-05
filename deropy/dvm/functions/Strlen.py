from deropy.dvm.functions.Function import Function


class Strlen(Function):
    def __init__(self):
        func_parameters = {
            "s": {"type": "str", "value": None},
        }
        super().__init__("strlen", 20_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["s"]["value"] = kwargs["s"]
        return len(kwargs["s"])

    def _computeGasStorageCost(self):
        return 0


def strlen(s: str):
    return Strlen()(s=s)
