import importlib
import sys
import os


from deropy.wallet.wallet_simulator import WalletSimulator
from deropy.dvm.Smartcontract import SmartContract


def clean_simulator():
    SmartContract.get_instance()._initialize()
    WalletSimulator.reset()


def simulator_setup(python_sc_path: str, cls_name: str): 
    global simulator, sc

    simulator = False
    if 'API_PATH' in os.environ:
        sys.path.append(os.path.dirname(os.environ['API_PATH']))

        # Import the class Lottery from the file loterry_api.py
        module = importlib.import_module(os.path.basename(os.environ['API_PATH']).split('.')[0])
        sc = getattr(module, cls_name)
        simulator = True
        return simulator, sc
    else:
        module = importlib.import_module(python_sc_path)
        sc = getattr(module, cls_name)
        return simulator, sc
