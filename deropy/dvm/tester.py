import importlib
import sys
import os


def simulator_setup(python_sc_path: str, cls_name: str): 
    global simulator, SmartContract

    simulator = False
    if 'API_PATH' in os.environ:
        sys.path.append(os.path.dirname(os.environ['API_PATH']))

        # Import the class Lottery from the file loterry_api.py
        module = importlib.import_module(os.path.basename(os.environ['API_PATH']).split('.')[0])
        SmartContract = getattr(module, cls_name)
        simulator = True
        return simulator, SmartContract
    else:
        module = importlib.import_module(python_sc_path)
        SmartContract = getattr(module, cls_name)
        return simulator, SmartContract
