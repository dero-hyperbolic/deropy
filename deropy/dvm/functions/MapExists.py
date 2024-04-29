from deropy.dvm.functions.Function import Function


class MapExists(Function):
    def __init__(self):
        func_parameters = {
            'key': {"type": "str", "value": None},
        }
        super().__init__("mapexist", 1000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters['key']['value'] = kwargs['key']
        return kwargs['key'] in self.sc.memory

    def _computeGasStorageCost(self):
        return 0


def map_exists(key: str):
    return MapExists()(key=key)
