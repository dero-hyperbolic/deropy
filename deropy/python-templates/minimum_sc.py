from deropy.dvm.functions import store, load, signer, exists
from deropy.dvm.Smartcontract import SmartContract

class Storage:
    def Initialize() -> int:
        if exists("owner") == 0:
            store("owner", signer())
            store("original_owner", 0)
        else:
            return 1
    

if __name__ == '__main__':
    import inspect
    sc = SmartContract()

    # Initialize the storage
    cg, sg = [], []

    print('----------------------------')
    sc.gasCompute, sc.gasStorage = [], []
    Storage.Initialize()
    print(sum(sc.gasCompute), sum(sc.gasStorage))

    print('----------------------------')
    sc.gasCompute, sc.gasStorage = [], []
    Storage.UpdateCode(inspect.getsource(Storage))
    print(sum(sc.gasCompute), sum(sc.gasStorage))