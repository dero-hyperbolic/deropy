from deropy.wallet.wallet_factory import WalletFactory
from deropy.dvm.tester import simulator_setup


simulator, SmartContractClass = simulator_setup('deropy.python_templates.nameservice', 'NameService')
wl_hyperbolic = WalletFactory.create_wallet('hyperbolic', simulator)
wl_new = WalletFactory.create_wallet('new_owner', simulator)
wl_random = WalletFactory.create_wallet('random_user', simulator)
wl_hardcoded = WalletFactory.create_wallet_from_public_key('hardcoded', 'deto1qyvyeyzrcm2fzf6kyq7egkes2ufgny5xn77y6typhfx9s7w3mvyd5qqynr5hx')
sc = SmartContractClass()


class TestNameService:
    def test_inialized(self):
        wl_hyperbolic.invoke_sc_function(sc.Initialize)

    # Test the Register function
    def test_register_too_short_name(self):
        wl_hyperbolic.invoke_sc_function(sc.Register, "test")
        storage = sc.read()
        assert "test" not in storage

    def test_register(self):
        wl_hyperbolic.invoke_sc_function(sc.Register, "hyperbolic")
        storage = sc.read()
        assert "hyperbolic" in storage
        assert storage["hyperbolic"] == wl_hyperbolic.raw_address

    def test_register_name_already_exists(self):
        wl_random.invoke_sc_function(sc.Register, "hyperbolic")
        storage = sc.read()
        assert "hyperbolic" in storage
        assert storage["hyperbolic"] == wl_hyperbolic.raw_address

    # Test the TransferOwnership function
    def test_transfer_ownership(self):
        wl_hyperbolic.invoke_sc_function(sc.TransferOwnership, ("hyperbolic", wl_new.string_address))
        storage = sc.read()
        assert storage["hyperbolic"] == wl_new.raw_address

    def test_transfer_ownership_wrong_owner(self):
        wl_random.invoke_sc_function(sc.TransferOwnership, ("hyperbolic", wl_new.string_address))
        storage = sc.read()
        assert storage["hyperbolic"] == wl_new.raw_address
        assert storage["hyperbolic"] != wl_random.raw_address
        assert storage["hyperbolic"] != wl_hyperbolic.raw_address