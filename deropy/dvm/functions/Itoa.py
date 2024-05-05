from deropy.dvm.functions.Function import Function


class Itoa(Function):
    def __init__(self):
        func_parameters = {
            "n": {"type": "int", "value": None},
        }
        super().__init__("itoa", 5_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["n"]["value"] = kwargs["n"]

        try:
            return int(str(kwargs["n"]))
        except Exception:
            raise ValueError(f"ITOA({kwargs['s']}) failed")

    def _computeGasStorageCost(self):
        return 0


def itoa(n: str):
    return Itoa()(n=n)
