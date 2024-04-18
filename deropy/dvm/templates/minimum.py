from deropy.dvm.functions.Exists import exists
from deropy.dvm.functions.Load import load
from deropy.dvm.functions.Store import store
from deropy.dvm.functions.Signer import signer
from deropy.dvm.sc import SmartContract

class Storage:
    def Initialize() -> int:
        if exists("owner") == 0:
            store("owner", signer())
            store("original_owner", 0)
        else:
            return 1
    
    def UpdateCode(code: str) -> int:
        if load("owner") != signer():
            return 1
        
        store("code", code)
        store("code", load("code") + code)

        a: int = 0
        b: int = 0
        while a < 10:
            a = a + 1
            b = b + 1
        return 0
    

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
