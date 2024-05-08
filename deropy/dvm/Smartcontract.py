from hashlib import sha256
import functools
import time

from deropy.dvm.utils import print_red


class SmartContract:
    scid = None
    active_wallet = None
    public_functions = []
    max_compute_gaz = 10_000_000
    max_storage_gas = 20_000
    dero_value = None
    asset_value = None

    # Blockchain basic component simulation
    blocks = []
    transactions = []
    scid = sha256(str(time.time()).encode()).hexdigest()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SmartContract, cls).__new__(cls)
            cls.instance._initialize()

        if SmartContract.scid is None:
            SmartContract.scid = sha256(str(time.time()*2).encode()).hexdigest()

        return cls.instance

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SmartContract, cls).__new__(cls)
            cls.instance._initialize()
        return cls.instance

    def _initialize(self):
        SmartContract.storage = dict()
        SmartContract.memory = dict()
        SmartContract.gasStorage = []
        SmartContract.gasCompute = []

        # At first instanciaion, create the smart-contract Id
        if SmartContract.scid is None:
            SmartContract.scid = sha256(str(time.time()*2).encode()).hexdigest()

    def read(self):
        return SmartContract.storage

    def store(self, key, value):
        SmartContract.storage[key] = value

    def load(self, key):
        return SmartContract.storage[key]

    @staticmethod
    def send_dero_with_tx(amount):
        SmartContract.dero_value = amount

    @staticmethod
    def send_asset_with_tx(amount, asset_id):
        if SmartContract.asset_value is None:
            SmartContract.asset_value = {}

        SmartContract.asset_value[asset_id] = amount


def isPublic(func):
    # A public method is one called during a transaction, therefore we should create a txid and store into a block
    def public_function(*args, **kwargs):
        sc = SmartContract.get_instance()

        # Create a transaction id and block id
        txid = sha256(str(time.time()).encode()).hexdigest()
        blockid = sha256(str(time.time()).encode()).hexdigest()

        # Store the transaction and the block
        SmartContract.transactions.append({
            "txid": txid,
            "blockid": blockid,
            "scid": sc.scid,
            "func": func.__name__,
            "args": args,
            "kwargs": kwargs
        })
        SmartContract.blocks.append(blockid)

        # Call the function
        return func(*args, **kwargs)

    public_function.is_public = True
    public_function.func_name = func.__name__
    return public_function


def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sc = SmartContract.get_instance()
        sc.gasCompute = []
        sc.gasStorage = []

        print("-" * 120)
        print("Function: ", func.func_name)
        value = func(*args, **kwargs)
        print('----')

        if sum(sc.gasCompute) > SmartContract.max_compute_gaz:
            print_red('total gas compute: ', sum(sc.gasCompute))
            print_red('total gas storage: ', sum(sc.gasStorage))
        else:
            print('total gas compute: ', sum(sc.gasCompute))
            print('total gas storage: ', sum(sc.gasStorage))

        if func.is_public:
            print("BLID: ", SmartContract.blocks[-1])
            print("TXID: ", SmartContract.transactions[-1]["txid"])

        return value

    return wrapper


def sc_logger(decorator, cls=None):
    if cls is None:
        return lambda cls: sc_logger(decorator, cls)

    class Decoratable(cls):
        def __init__(self, *args, **kargs):
            super().__init__(*args, **kargs)

        def __getattribute__(self, item):
            value = object.__getattribute__(self, item)
            if callable(value):
                # if the function start with a capital letter, it is a public function, and need to be wrapped
                if value.__name__[0].isupper():
                    SmartContract.public_functions.append(value.__name__)

                    # wrap the function with the isPublic decorator
                    return decorator(isPublic(value))
            return value

    return Decoratable


if __name__ == "__main__":
    sc = SmartContract()
    sc.storage["key"] = "value"
    sc2 = SmartContract.get_instance()
    print(sc.storage["key"])
    print(sc2.storage["key"])
    print(sc == sc2)
