from deropy.dvm.functions import exists, store, load, strlen, signer, address_raw
from deropy.dvm.Smartcontract import SmartContract, logger, sc_logger


@sc_logger(logger)
class NameService(SmartContract):

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
    from deropy.dvm.Wallet import WalletSimulator

    # Let define three wallets
    WalletSimulator.create_wallet('hyperbolic')
    WalletSimulator.create_wallet('new_owner')
    WalletSimulator.create_wallet('random_user')
    WalletSimulator.create_wallet_from_public_key("deto1qyvyeyzrcm2fzf6kyq7egkes2ufgny5xn77y6typhfx9s7w3mvyd5qqynr5hx")

    WalletSimulator.active_wallet = 'hyperbolic'

    # configure the test scenario
    sc = NameService()

    # Initialize the smart contract (akin to deployement on the blockchain)
    sc.Initialize()

    # Test the Register function
    assert sc.Register("test") == 0
    assert "test" not in SmartContract.get_instance().storage

    assert sc.Register("hyperbolic") == 0
    assert "hyperbolic" in SmartContract.get_instance().storage
    assert SmartContract.get_instance().storage["hyperbolic"] == WalletSimulator.get_raw_address_from_id('hyperbolic')

    # ---- Somebody else cannot claim that name anymore
    WalletSimulator.active_wallet = 'random_user'
    assert sc.Register("hyperbolic") == 0
    assert "hyperbolic" in SmartContract.get_instance().storage
    assert SmartContract.get_instance().storage["hyperbolic"] == WalletSimulator.get_raw_address_from_id('hyperbolic')

    # ---- Until the original owner transfer the ownership
    WalletSimulator.active_wallet = 'hyperbolic'
    sc.TransferOwnership("hyperbolic", WalletSimulator.get_string_address_from_id('new_owner'))
    assert SmartContract.get_instance().storage["hyperbolic"] == WalletSimulator.get_raw_address_from_id('new_owner')
