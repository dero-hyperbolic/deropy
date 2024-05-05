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
    from deropy.dvm.Wallet import WalletSimulator, Wallet

    # Let define three wallets
    wl_hyperbolic: Wallet = WalletSimulator.create_wallet('hyperbolic')
    wl_no: Wallet = WalletSimulator.create_wallet('new_owner')
    wl_random: Wallet = WalletSimulator.create_wallet('random_user')
    WalletSimulator.create_wallet_from_public_key("deto1qyvyeyzrcm2fzf6kyq7egkes2ufgny5xn77y6typhfx9s7w3mvyd5qqynr5hx")

    sc = NameService()

    # Initialize the smart contract (akin to deployement on the blockchain)
    wl_hyperbolic.invoke_sc_function(sc.Initialize)

    # Test the Register function
    wl_hyperbolic.invoke_sc_function(sc.Register, "test")
    assert "test" not in SmartContract.get_instance().storage

    wl_hyperbolic.invoke_sc_function(sc.Register, "hyperbolic")
    assert "hyperbolic" in SmartContract.get_instance().storage
    assert SmartContract.get_instance().storage["hyperbolic"] == wl_hyperbolic.raw_address

    # ---- Somebody else cannot claim that name anymore
    wl_random.invoke_sc_function(sc.Register, "hyperbolic")
    assert "hyperbolic" in SmartContract.get_instance().storage
    assert SmartContract.get_instance().storage["hyperbolic"] == wl_hyperbolic.raw_address

    # ---- Until the original owner transfer the ownership
    WalletSimulator.active_wallet = 'hyperbolic'
    wl_hyperbolic.invoke_sc_function(sc.TransferOwnership, ("hyperbolic", wl_no.string_address))
    assert SmartContract.get_instance().storage["hyperbolic"] == wl_no.raw_address
