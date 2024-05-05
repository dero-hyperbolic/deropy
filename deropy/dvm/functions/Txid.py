from deropy.dvm.functions.Function import Function


class Txid(Function):
    def __init__(self):
        func_parameters = {
            'value': {"type": "int", "value": None},
        }
        super().__init__("txid", 2000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        raise NotImplementedError("This function is not implemented yet")

    def _computeGasStorageCost(self):
        return 0


def txid():
    return Txid()()
