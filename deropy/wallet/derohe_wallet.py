import requests
import time


from deropy.utils import active_waiting
from deropy.wallet.wallet import Wallet


class DeroheWallet(Wallet):
    def __init__(self, name, id):
        super().__init__(name, id)

    def _init(self):
        wallet_port = 30000 + self.id
        self.rpc_host = f'http://127.0.0.1:{wallet_port}/json_rpc'

        self.logger.info(f'Fetching wallet information for "{self.name}"')
        self.string_address = self._get_string_address()
        self.raw_address = self._get_raw_address()

        self.logger.info(f'Wallet "{self.name}" created: {self.string_address} - {self.raw_address} - "{self.name}')
        self.balance = {}

    def _get_string_address(self):
        payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "GetAddress"
        }
        response = requests.post(self.rpc_host, json=payload).json()
        return response['result']['address']

    def get_raw_address(self):
        return self.raw_address

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

    def get_balance(self, token):
        payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "GetBalance",
            "params": {
                "scid": token
            }
        }
        response = requests.post(self.rpc_host, json=payload).json()
        return response['result']['balance']

    def set_balance(self, token, amount):
        self.balance[token] = amount

    def invoke_sc_function(self, func, func_args: tuple = None, dero_deposit: int = None, asset_deposit: tuple = None):
        super().invoke_sc_function(func, func_args, dero_deposit, asset_deposit)
        args = [] if func_args is None else (func_args, ) if isinstance(func_args, (int, str)) else func_args
        kwargs = {'dero_deposit': dero_deposit, 'asset_deposit': asset_deposit, 'host': self.rpc_host}

        result = func(*args, **kwargs)
        self.logger.debug('in simulator, waiting 2 seconds to simulate transaction')
        time.sleep(2)
        return result
