from deropy.dvm.functions.Function import Function
from Crypto.Hash import keccak


class Keccak256(Function):
    def __init__(self):
        func_parameters = {
            "s": {"type": "str", "value": None},
        }
        super().__init__("keccak256", 25_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["s"]["value"] = kwargs["s"]
        k = keccak.new(digest_bits=256)
        k.update(kwargs["s"].encode())
        return k.hexdigest()

    def _computeGasStorageCost(self):
        return 0


def keccak256(s: str):
    return Keccak256()(s=s)
