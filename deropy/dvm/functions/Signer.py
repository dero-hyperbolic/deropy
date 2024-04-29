from deropy.dvm.functions.Function import Function
from deropy.dvm.Wallet import WalletSimulator


class Signer(Function):
    def __init__(self):
        func_parameters = {}
        super().__init__("signer", 5_000, 0, func_parameters)

    def _exec(self, *args, **kwargs):
        if not WalletSimulator.is_initialized():
            raise Exception("Wallet simulator not initialized")
        if WalletSimulator.active_wallet is None:
            raise Exception("No active wallet")

        return WalletSimulator.get_raw_address()

    def _computeGasStorageCost(self):
        return 0


def signer():
    return Signer()()
