from deropy.dvm.functions.Function import Function


class Panic(Function):
    def __init__(self):
        func_parameters = {}
        super().__init__("random", 1000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        raise RuntimeError("Panic")

    def _computeGasStorageCost(self):
        return 0


def panic():
    return Panic()()
