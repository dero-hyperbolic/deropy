from deropy.dvm.functions.Function import Function


class Delete(Function):
    def __init__(self):
        func_parameters = {
            'key': {"type": "str", "value": None},
        }
        super().__init__("delete", 3000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters['key']['value'] = kwargs['key']
        del self.sc.storage[kwargs['key']]

    def _computeGasStorageCost(self):
        return 0


def delete(key: str):
    return Delete()(key=key)
