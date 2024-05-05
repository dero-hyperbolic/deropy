from deropy.dvm.Smartcontract import SmartContract
from deropy.dvm.Wallet import WalletSimulator, Wallet
from deropy.python_templates.Nameservice import NameService

# Let define three wallets
wl_hyperbolic: Wallet = WalletSimulator.create_wallet('hyperbolic')
wl_new: Wallet = WalletSimulator.create_wallet('new_owner')
wl_random: Wallet = WalletSimulator.create_wallet('random_user')
wl_fixed: Wallet = WalletSimulator.create_wallet_from_public_key('hardcoded', 'deto1qyvyeyzrcm2fzf6kyq7egkes2ufgny5xn77y6typhfx9s7w3mvyd5qqynr5hx')

# configure the test scenario
sc = NameService()


class TestNameService:
    def test_inialized(self):
        wl_hyperbolic.invoke_sc_function(sc.Initialize)

    # Test the Register function
    def test_register_too_short_name(self):
        wl_hyperbolic.invoke_sc_function(sc.Register, "test")
        assert "test" not in SmartContract.get_instance().storage

    def test_register(self):
        wl_hyperbolic.invoke_sc_function(sc.Register, "hyperbolic")
        assert "hyperbolic" in SmartContract.get_instance().storage
        assert SmartContract.get_instance().storage["hyperbolic"] == wl_hyperbolic.raw_address

    def test_register_name_already_exists(self):
        wl_random.invoke_sc_function(sc.Register, "hyperbolic")
        assert "hyperbolic" in SmartContract.get_instance().storage
        assert SmartContract.get_instance().storage["hyperbolic"] == wl_hyperbolic.raw_address

    # Test the TransferOwnership function
    def test_transfer_ownership(self):
        wl_hyperbolic.invoke_sc_function(sc.TransferOwnership, ("hyperbolic", wl_new.string_address))
        assert SmartContract.get_instance().storage["hyperbolic"] == wl_new.raw_address

    def test_transfer_ownership_wrong_owner(self):
        wl_random.invoke_sc_function(sc.TransferOwnership, ("hyperbolic", wl_new.string_address))
        assert SmartContract.get_instance().storage["hyperbolic"] == wl_new.raw_address
        assert SmartContract.get_instance().storage["hyperbolic"] != wl_random.raw_address
        assert SmartContract.get_instance().storage["hyperbolic"] != wl_hyperbolic.raw_address