import logging


from deropy.dvm.Smartcontract import SmartContract
from deropy.wallet.wallet_simulator import WalletSimulator


class Wallet:
    def __init__(self, name, id, simulator: bool = False):
        self.logger = logging.getLogger('deropy')
        self.logger.info(f'Creating wallet "{name}" (simulator: {simulator})')
        self.raw_address = None
        self.string_address = None
        self.name = name
        self.id = id

        self._init()

    def _init(self):
        raise NotImplementedError

    def get_balance(self, token):
        raise NotImplementedError

    def set_balance(self, token, amount):
        raise NotImplementedError

    @classmethod
    def from_public_key(cls, public_key):
        wallet = cls(public_key, 1000)
        wallet.string_address = public_key
        wallet.raw_address = public_key[:33]
        return wallet

    def invoke_sc_function(self, func, func_args: tuple = None, dero_deposit: int = None, asset_deposit: tuple = None):
        self.logger.info(f'Invoking function "{func.__name__}({func_args})" in wallet "{self.name}" using {dero_deposit} DERO and {asset_deposit} assets')
        WalletSimulator.active_wallet = self

        if dero_deposit is not None:
            SmartContract.send_dero_with_tx(dero_deposit)
        if asset_deposit is not None:
            SmartContract.send_asset_with_tx(asset_deposit[0], asset_deposit[1])
