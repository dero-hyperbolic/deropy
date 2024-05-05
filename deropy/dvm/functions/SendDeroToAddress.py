from deropy.dvm.functions.Function import Function
from deropy.dvm.Wallet import WalletSimulator, Wallet


class SendDeroToAddress(Function):
    def __init__(self):
        func_parameters = {
            "raw_address": {"type": "str", "value": None},
            "amount": {"type": "int", "value": None},
        }
        super().__init__("send_dero_to_address", 70_000, 0, func_parameters)

    def _computeGasStorageCost(self):
        return len(self.parameters["raw_address"]["value"])

    def _exec(self, *args, **kwargs):
        if WalletSimulator.is_initialized() is False:
            raise RuntimeError("WalletSimulator is not initialized")
        if WalletSimulator.active_wallet is None:
            raise RuntimeError("No active wallet")
        
        self.parameters["raw_address"]["value"] = kwargs["raw_address"]
        self.parameters["amount"]["value"] = kwargs["amount"]

        destination_wallet: Wallet = WalletSimulator.get_wallet_from_raw(self.parameters["raw_address"]["value"])
        if destination_wallet is None:
            return 1
        
        destination_wallet.set_balance("DERO", self.parameters["amount"]["value"])
        return 0


def send_dero_to_address(raw_address: str, amount: int):
    return SendDeroToAddress()(raw_address=raw_address, amount=amount)
