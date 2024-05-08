import hashlib
import requests
import time
from deropy.dvm.Smartcontract import SmartContract


class Wallet:
    def __init__(self, name, id, simulator: bool = False):
        print(f'Creating wallet "{name}" (simulator: {simulator})')
        self.name = name
        self.id = id
        self.simulator = simulator
        wallet_port = 30000 + self.id
        self.rpc_host = f'http://127.0.0.1:{wallet_port}/json_rpc'

        if not simulator:
            self._python_init()
        else:
            self._simulator_init()

    def _python_init(self):
        self.string_address = hashlib.sha256(str(self.name).encode()).hexdigest()
        self.raw_address = self.string_address[:33]
        self.balance = {}

    def _simulator_init(self):
        self.string_address = self._get_string_address()
        self.raw_address = self._get_raw_address()

        print(f'Wallet "{self.name}" created: {self.string_address} - {self.raw_address} - "{self.name}')
        self.balance = {}

    def _get_string_address(self):
        payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "GetAddress"
        }
        response = requests.post(self.rpc_host, json=payload).json()
        return response['result']['address']

    def _get_raw_address(self):
        def register(self, timeout=0):
            payload = {
                "jsonrpc": "2.0",
                "id": "1",
                "method": "scinvoke",
                "params": {
                    "scid": "0000000000000000000000000000000000000000000000000000000000000001",
                    "ringsize": 2,
                    "sc_rpc": [
                        {
                            "name": "entrypoint",
                            "datatype": "S",
                            "value": "Register"
                        },
                        {
                            "name": "name",
                            "datatype": "S",
                            "value": self.name
                        }
                    ]
                }
            }
            response = requests.post(self.rpc_host, json=payload).json()
            
            if "error" in response:
                waiting_time = 5
                active_waiting(f'Wallet not yet registered, trying again in {waiting_time}', waiting_time)
                return register(self, timeout + waiting_time)
            return response

        def get_raw_address(self):
            time.sleep(2)
            url = 'http://127.0.0.1:20000/json_rpc'
            payload = {
                "jsonrpc": "2.0",
                "id": "1",
                "method": "DERO.GetSC",
                "params": {
                    "scid": "0000000000000000000000000000000000000000000000000000000000000001",
                    "code": True,
                    "variables": True
                }
            }
            response = requests.post(url, json=payload).json()
            return response['result']['stringkeys'][self.name]

        register(self)
        return get_raw_address(self)

    @classmethod
    def from_public_key(cls, public_key):
        wallet = cls(public_key, 1000)
        wallet.string_address = public_key
        wallet.raw_address = public_key[:33]
        return wallet

    def invoke_sc_function(self, func, func_args: tuple = None, dero_deposit: int = None, asset_deposit: tuple = None):
        print(f'Invoking function "{func.__name__}({func_args})" in wallet "{self.name}" using {dero_deposit} DERO and {asset_deposit} assets')
        WalletSimulator.active_wallet = self.name

        if dero_deposit is not None:
            SmartContract.send_dero_with_tx(dero_deposit)
        if asset_deposit is not None:
            SmartContract.send_asset_with_tx(asset_deposit[0], asset_deposit[1])

        # Prepare the SC function parameters (can change if running in simulator)
        args = [] if func_args is None else (func_args, ) if isinstance(func_args, (int, str)) else func_args
        kwargs = {'dero_deposit': dero_deposit, 'asset_deposit': asset_deposit, 'host': self.rpc_host}

        if self.simulator:
            result = func(*args, **kwargs)
            print('in simulator, waiting 2 seconds to simulate transaction')
            time.sleep(2)
            return result

        return func(*args)

    def get_balance(self, token):
        return self.balance.get(token, 0)

    def set_balance(self, token, amount):
        self.balance[token] = amount


class WalletSimulator:
    active_wallet = None
    wallets = {}
    wallet_count = 0

    @staticmethod
    def create_wallet(name, simulator: bool = False):
        if WalletSimulator.wallet_count >= 20:
            raise Exception("Maximum number of wallets reached")
        
        WalletSimulator.wallets[name] = Wallet(name, WalletSimulator.wallet_count, simulator)
        WalletSimulator.wallet_count += 1
        return WalletSimulator.wallets[name]

    @staticmethod
    def create_wallet_from_public_key(name, public_key):
        WalletSimulator.wallets[name] = Wallet.from_public_key(public_key)

    @staticmethod
    def find_wallet_id_from_string(string_address):
        for id, wallet in WalletSimulator.wallets.items():
            if wallet.string_address == string_address:
                return id
        raise Exception("Wallet not found")

    @staticmethod
    def find_wallet_id_from_raw(raw_address):
        for id, wallet in WalletSimulator.wallets.items():
            if wallet.raw_address == raw_address:
                return id
        raise Exception("Wallet not found")
    
    @staticmethod
    def get_wallet_from_raw(raw_address):
        id = WalletSimulator.find_wallet_id_from_raw(raw_address)
        return WalletSimulator.get_wallet_from_id(id)
    
    @staticmethod
    def get_wallet_from_id(id):
        return WalletSimulator.wallets[id]

    @staticmethod
    def get_raw_address():
        return WalletSimulator.wallets[WalletSimulator.active_wallet].raw_address

    @staticmethod
    def get_string_address():
        return WalletSimulator.wallets[WalletSimulator.active_wallet].string_address

    @staticmethod
    def get_raw_address_from_id(id):
        return WalletSimulator.wallets[id].raw_address

    def get_string_address_from_id(id):
        return WalletSimulator.wallets[id].string_address

    @staticmethod
    def is_initialized():
        return WalletSimulator.active_wallet is not None
    

def active_waiting(msg: str, timeout: int):
    start = time.time()

    while time.time() - start < timeout:
        for char in ['|', '/', '-', '\\']:
            print(f'{msg} {char}', end='\r')
            time.sleep(0.1)
    print('')