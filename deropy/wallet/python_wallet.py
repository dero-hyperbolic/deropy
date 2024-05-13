import hashlib


from deropy.dvm.Smartcontract import SmartContract
from deropy.wallet.wallet import Wallet


class PythonWallet(Wallet):
    def __init__(self, name, id):
        super().__init__(self, name, id)

    def _init(self):
        self.string_address = hashlib.sha256(str(self.name).encode()).hexdigest()
        self.raw_address = self.string_address[:33]
        self.balance = {}

    def _get_string_address(self):
        return self.string_address

    def get_raw_address(self):
        # return self.raw_address
        return "".join("{:02x}".format(c) for c in self.raw_address.encode())

    def get_balance(self, token):
        return self.balance.get(token, 0)

    def set_balance(self, token, amount):
        self.balance[token] = amount

    def invoke_sc_function(self, func, func_args: tuple = None, dero_deposit: int = None, asset_deposit: tuple = None):
        super().invoke_sc_function(func, func_args, dero_deposit, asset_deposit)

        # Wallet balance is consumed the dero or / and asset deposit
        # if dero_deposit is not None:
        #     self.balance["DERO"] -= dero_deposit
        if asset_deposit is not None:
            self.balance[SmartContract.SCID] -= asset_deposit[0]

        args = [] if func_args is None else (func_args, ) if isinstance(func_args, (int, str)) else func_args
        result = func(*args)

        # deposit is burned by the smart-contract
        SmartContract.dero_value = None
        SmartContract.asset_value = None

        return result
