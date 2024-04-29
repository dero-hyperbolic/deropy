import hashlib


class Wallet:
    def __init__(self, id):
        self.string_address = hashlib.sha256(str(id).encode()).hexdigest()
        self.raw_address = self.string_address[:33]
        self.balance = 0


class WalletSimulator:
    active_wallet = None
    wallets = {}

    @staticmethod
    def create_wallet(id):
        WalletSimulator.wallets[id] = Wallet(id)

    @staticmethod
    def find_wallet_id_from_string(self, string_address):
        for id, wallet in WalletSimulator.wallets.items():
            if wallet.string_address == string_address:
                return id
            
    @staticmethod
    def find_wallet_id_from_raw(self, raw_address):
        for id, wallet in WalletSimulator.wallets.items():
            if wallet.raw_address == raw_address:
                return id
            
    @staticmethod
    def is_initialized():
        return WalletSimulator.active_wallet is not None
                
            