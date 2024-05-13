from deropy.dvm.functions.Function import Function


class Hex(Function):
    def __init__(self):
        func_parameters = {
            "s": {"type": "str", "value": None},
        }
        super().__init__("hex", 10_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["s"]["value"] = kwargs["s"]
        return "".join("{:02x}".format(c) for c in kwargs["s"].encode())

    def _computeGasStorageCost(self):
        return 0


def hex(s: str):
    return Hex()(s=s)
