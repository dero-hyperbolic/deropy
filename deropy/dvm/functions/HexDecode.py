from deropy.dvm.functions.Function import Function


class HexDecode(Function):
    def __init__(self):
        func_parameters = {
            "s": {"type": "str", "value": None},
        }
        super().__init__("hex_decode", 10_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["s"]["value"] = kwargs["s"]
        return int(kwargs["s"], 16)

    def _computeGasStorageCost(self):
        return 0


def hex_decode(s: str):
    return HexDecode()(s=s)
