from deropy.dvm.Smartcontract import SmartContract
from deropy.dvm.utils import print_interpreter


class Function:
    def __init__(self, name, compute_cost, storage_cost, parameters: dict):
        self.sc = SmartContract.get_instance()
        self.name = name
        self.compute_cost = compute_cost
        self.storage_cost = storage_cost
        self.parameters = parameters

    def __str__(self):
        return self.name.upper()

    def _computeGasStorageCost(self):
        raise NotImplementedError

    def __call__(self, **kwargs):
        # Check if the argument provided in kwargs are identical to the parameters of the function
        for key, value in kwargs.items():
            if key not in self.parameters.keys():
                raise Exception(f"Invalid argument [{key}] provided to function {self.name}")

            if self.parameters[key]["type"] == "Any":
                continue

            # Check the parameters, since we are parsing the arguments as strings we need to convert them to the correct type
            if self.parameters[key]["type"] == "int":
                try:
                    kwargs[key] = int(value)
                except Exception:
                    raise Exception(
                        f"Invalid type [str] for argument [{key}] provided to function [{self.name}], expected [int]")

        value = self._exec(**kwargs)

        # build the message to be printed
        args = ', '.join([f'{value}' for key, value in kwargs.items()]) if kwargs else ''
        msg = [f'{self.name.upper()}({args})']
        self.sc.gasCompute.append(self.compute_cost)
        self.sc.gasStorage.append(self._computeGasStorageCost())
        msg += [f'computeGas: {self.compute_cost}', f'storageGas: {self._computeGasStorageCost()}']

        # print the message in three column of constant width
        print_interpreter(msg)
        return value
