from deropy.dvm.functions.Function import Function


class Exists(Function):
    def __init__(self):
        func_parameters = {
            'key': {"type": "str", "value": None},
        }
        super().__init__("exists", 5_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters['key']['value'] = kwargs['key']
        if kwargs['key'] in self.sc.storage:
            return 1
        return 0

    def _computeGasStorageCost(self):
        return 0


def exists(key: str):
    return Exists()(key=key)
