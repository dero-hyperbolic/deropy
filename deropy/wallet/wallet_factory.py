import logging


from deropy.wallet.wallet_simulator import WalletSimulator
from deropy.wallet.derohe_wallet import DeroheWallet
from deropy.wallet.python_wallet import PythonWallet


class WalletFactory:
    @staticmethod
    def create_wallet(name, simulator: bool = False):
        if name in WalletSimulator.wallets:
            return WalletSimulator.wallets[name]

        if WalletSimulator.wallet_count >= 20:
            raise Exception("Maximum number of wallets reached")

        if simulator:
            new_wallet = DeroheWallet(name, WalletSimulator.wallet_count)
        else:
            new_wallet = PythonWallet(name, WalletSimulator.wallet_count)

        WalletSimulator.wallets[name] = new_wallet
        WalletSimulator.wallet_count += 1
        return WalletSimulator.wallets[name]

    @staticmethod
    def create_wallet_from_public_key(name, public_key, simulator: bool = False):
        if simulator:
            WalletSimulator.wallets[name] = DeroheWallet.from_public_key(public_key)
        else:
            WalletSimulator.wallets[name] = PythonWallet.from_public_key(public_key)