from deropy.dvm.functions.Function import Function


class UpdateScCode(Function):
    def __init__(self):
        func_parameters = {
            "sc_code": {"type": "str", "value": None},
        }
        super().__init__("update_sc_code", 5000, 0, func_parameters)

    def _computeGasStorageCost(self):
        if isinstance(self.parameters["sc_code"]["value"], int):
            return 1
        else:
            size = len(self.parameters["sc_code"]["value"])
            return size * 2  # 2 gas per byte (1 for tx, 1 for storage)

    def _exec(self, *args, **kwargs):
        self.parameters["sc_code"]["value"] = kwargs["sc_code"]
        self.sc.storage["code"] = kwargs["sc_code"]
        return 0


def update_sc_code(sc_code: str):
    return UpdateScCode()(sc_code=sc_code)
