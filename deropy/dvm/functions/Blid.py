from deropy.dvm.functions.Function import Function


class Blid(Function):
    def __init__(self):
        func_parameters = {}
        super().__init__("blid", 2000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        raise NotImplementedError("This function is not implemented yet")

    def _computeGasStorageCost(self):
        return 0


def blid():
    return Blid()()
