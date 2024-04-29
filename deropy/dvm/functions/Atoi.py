from deropy.dvm.functions.Function import Function


class Atoi(Function):
    def __init__(self):
        func_parameters = {
            "s": {"type": "str", "value": None},
        }
        super().__init__("atoi", 5_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["s"]["value"] = kwargs["s"]

        try:
            return str(int(kwargs["s"]))
        except Exception:
            raise ValueError(f"ATOI({kwargs['s']}) failed")

    def _computeGasStorageCost(self):
        return 0


def atoi(s: str):
    return Atoi()(s=s)
