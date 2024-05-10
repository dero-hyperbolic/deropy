from deropy.wallet.wallet_factory import WalletFactory
from deropy.wallet.wallet_simulator import WalletSimulator
from deropy.dvm.Smartcontract import SmartContract


def clean_simulator():
    SmartContract.storage = {}
    SmartContract.dero_value = None
    SmartContract.asset_value = None

    WalletFactory.wallets = {}

    WalletSimulator.active_wallet = None
    WalletSimulator.wallet_count = 0