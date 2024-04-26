from deropy.dvm.functions import exists, store, load, strlen, signer, address_raw
from deropy.dvm.Smartcontract import SmartContract, logger, isPublic, sc_logger
from deropy.dvm.utils import get_address, get_raw_address

@sc_logger(logger)
class Storage(SmartContract):

    def Initialize(self) -> int:
        return 0

    def Register(self, name: str) -> int:
        if exists(name):
            return 0
        
        if strlen(name) >= 6:
            store(name, signer())
            return 0
        
        if signer() != address_raw("deto1qyvyeyzrcm2fzf6kyq7egkes2ufgny5xn77y6typhfx9s7w3mvyd5qqynr5hx"):
            return 0
    
    def TransferOwnership(self, name: str, new_owner: str) -> int:
        if load(name) != signer():
            return 1
        
        store(name, address_raw(new_owner))
        return 0



# We can now test the smart contract by creating a scenario.
# For more complexe SC, it will be necessary to create a proper test suite.
if __name__ == '__main__':
    original_signer = 'hyperbolic'
    new_owner = "new_owner"
    random_user = "random_user"

    # configure the test scenario
    SmartContract.active_wallet = get_address(original_signer)
    sc = Storage()

    # Initialize the smart contract (akin to deployement on the blockchain)
    sc.Initialize()
    
    # Test the Register function
    assert sc.Register("test") == 0
    assert "test" not in SmartContract.get_instance().storage

    assert sc.Register("hyperbolic") == 0
    assert "hyperbolic" in SmartContract.get_instance().storage
    assert SmartContract.get_instance().storage["hyperbolic"] == get_raw_address(original_signer)  

    # ---- Somebody else cannot claim that name anymore
    SmartContract.active_wallet = get_address(random_user)
    assert sc.Register("hyperbolic") == 0
    assert "hyperbolic" in SmartContract.get_instance().storage
    assert SmartContract.get_instance().storage["hyperbolic"] == get_raw_address(original_signer)

    # ---- Until the original owner transfer the ownership
    SmartContract.active_wallet = get_address(original_signer)
    sc.TransferOwnership("hyperbolic", get_address(new_owner))
    assert SmartContract.get_instance().storage["hyperbolic"] == get_raw_address(new_owner)
    