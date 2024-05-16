import pytest
from deropy.wallet.wallet_factory import WalletFactory
from deropy.dvm.tester import simulator_setup, clean_simulator


@pytest.fixture(scope='class', autouse=True)
def initialize_test_suite():
    global simulator, sc, SmartContract, wl_hyperbolic, wl_user1, wl_user2

    simulator, SmartContract = simulator_setup('deropy.python_templates.nameservice', 'NameService')
    wl_hyperbolic = WalletFactory.create_wallet('hyperbolic', simulator)
    wl_user1 = WalletFactory.create_wallet('wallet_user1', simulator)
    wl_user2 = WalletFactory.create_wallet('wallet_user2', simulator)
    sc = SmartContract()

    yield 

    clean_simulator()


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
        wl_user1.invoke_sc_function(sc.Register, "hyperbolic")
        storage = sc.read()
        assert "hyperbolic" in storage
        assert storage["hyperbolic"] == wl_hyperbolic.raw_address

    # Test the TransferOwnership function
    def test_transfer_ownership(self):
        wl_hyperbolic.invoke_sc_function(sc.TransferOwnership, ("hyperbolic", wl_user2.string_address))
        storage = sc.read()
        assert storage["hyperbolic"] == wl_user2.raw_address

    def test_transfer_ownership_wrong_owner(self):
        wl_user1.invoke_sc_function(sc.TransferOwnership, ("hyperbolic", wl_user2.string_address))
        storage = sc.read()
        assert storage["hyperbolic"] == wl_user2.raw_address
        assert storage["hyperbolic"] != wl_user1.raw_address
        assert storage["hyperbolic"] != wl_hyperbolic.raw_address