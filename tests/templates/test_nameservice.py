from deropy.wallet import WalletSimulator
from deropy.dvm.tester import simulator_setup


# By default there is two global variables created by the simulator_setup fixture
# simulator: boolean that indicates if the tests are running in a simulator
# SmartContract: the class of the smart contract

# The function simulator_setup has to be called with a function that setups the wallets
# its role is to ensure that the wallets are associated with the simulator json_rpc endpoints to
# correspond to the wallets already created in the simulator


global simulator, SmartContract
simulator = False
SmartContract = None


# call the simulator_setup fixture to setup the simulator
simulator, SmartContract = simulator_setup('deropy.python_templates.Nameservice', 'NameService')
wl_hyperbolic = WalletSimulator.create_wallet('hyperbolic', simulator)
wl_new = WalletSimulator.create_wallet('new_owner', simulator)
wl_random = WalletSimulator.create_wallet('random_user', simulator)
wl_hardcoded = WalletSimulator.create_wallet_from_public_key('hardcoded', 'deto1qyvyeyzrcm2fzf6kyq7egkes2ufgny5xn77y6typhfx9s7w3mvyd5qqynr5hx')
sc = SmartContract()


class TestNameService:
    def test_inialized(self):
        wl_hyperbolic.invoke_sc_function(sc.Initialize)

    # Test the Register function
    def test_register_too_short_name(self):
        wl_hyperbolic.invoke_sc_function(sc.Register, "test")
        current_storage = sc.read()
        assert "test" not in current_storage

    def test_register(self):
        wl_hyperbolic.invoke_sc_function(sc.Register, "hyperbolic")
        current_storage = sc.read()
        assert "hyperbolic" in current_storage
        assert current_storage["hyperbolic"] == wl_hyperbolic.raw_address

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