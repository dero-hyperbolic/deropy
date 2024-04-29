from deropy.dvm.functions.Function import Function
import hashlib


class Sha256(Function):
    def __init__(self):
        func_parameters = {
            "s": {"type": "str", "value": None},
        }
        super().__init__("sha256", 25_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["s"]["value"] = kwargs["s"]
        return hashlib.sha256(kwargs["s"].encode()).hexdigest()

    def _computeGasStorageCost(self):
        return 0


def sha256(s: str):
    return Sha256()(s=s)
