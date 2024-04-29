from deropy.dvm.functions.Function import Function
from deropy.dvm.Wallet import WalletSimulator


class AddressRaw(Function):
    def __init__(self):
        func_parameters = {
            "address": {"type": "str", "value": None},
        }
        super().__init__("address_raw", 60_000, 0, func_parameters)

    def _computeGasStorageCost(self):
        return 0

    def _exec(self, *args, **kwargs):
        address = self.parameters["address"]["value"] = kwargs["address"]

        if not WalletSimulator.is_initialized():
            raise Exception("Wallet simulator not initialized")
        if WalletSimulator.active_wallet is None:
            raise Exception("No active wallet")

        self.parameters["address"]["value"] = address
        wallet_id = WalletSimulator.find_wallet_id_from_string(address)
        return WalletSimulator.wallets[wallet_id].raw_address


def address_raw(address: str):
    return AddressRaw()(address=address)
