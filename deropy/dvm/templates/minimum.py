from deropy.dvm.functions.Exists import exists, exists_dero
from deropy.dvm.functions.Load import load, load_dero
from deropy.dvm.functions.Store import store, store_dero
from deropy.dvm.functions.Signer import signer
from deropy.dvm.functions.Return import ret, ret_dero
from deropy.dvm.sc import SmartContract
from deropy.dvm.utils import flatten_list

class Storage:
    def Initialize() -> int:
        if exists("owner") == 0:
            store("owner", signer())
            store("original_owner", 0)
        return 0
    
    def UpdateCode(code: str) -> int:
        if load("owner") != signer():
            a: int = 0
            b : int = 0
        else:
            c: int = 0
            d: int = 0
        
        previous_code: str = load("code")
        store("code", previous_code + code)
        store("code", load("code") + code)

        while a < 10:
            a = a + 1
            b = b + 1
        return 0
    
    # def Register(bounty: int, size: int, duration: int) -> int:
    #     a: str = 0
    #     a = a / 1000
    #     return 0
