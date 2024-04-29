from deropy.dvm.functions.Function import Function


class Substr(Function):
    def __init__(self):
        func_parameters = {
            "s": {"type": "str", "value": None},
            "offset": {"type": "int", "value": None},
            "lenght": {"type": "int", "value": None},
        }
        super().__init__("strlen", 20_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        self.parameters["s"]["value"] = kwargs["s"]
        self.parameters["offset"]["value"] = kwargs["offset"]
        self.parameters["lenght"]["value"] = kwargs["lenght"]

        start_position = kwargs["offset"]
        end_position = start_position + kwargs["lenght"]
        return len(kwargs["s"][start_position:end_position])

    def _computeGasStorageCost(self):
        return 0


def substr(s: str, offset: int, lenght: int):
    return Substr()(s=s, offset=offset, lenght=lenght)
