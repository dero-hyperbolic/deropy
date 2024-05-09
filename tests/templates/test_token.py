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
simulator, SmartContract = simulator_setup('deropy.python_templates.token', 'Token')
wl_hyperbolic = WalletSimulator.create_wallet('hyperbolic', simulator)
wl_random = WalletSimulator.create_wallet('random_user', simulator)
sc = SmartContract()


class TestNameService:
    def test_inialized(self):
        wl_hyperbolic.invoke_sc_function(sc.InitializePrivate)
        current_storage = SmartContract.get_instance().storage
        assert current_storage['owner'] == wl_hyperbolic.raw_address

    def test_initialize_cant_be_called_twice(self):
        wl_random.invoke_sc_function(sc.InitializePrivate)
        current_storage = SmartContract.get_instance().storage
        assert current_storage['owner'] == wl_hyperbolic.raw_address

    def test_issue_token(self):
        wl_hyperbolic.invoke_sc_function(sc.IssueTokenX, dero_deposit=100)

    def test_convert_token(self):
        wl_hyperbolic.invoke_sc_function(sc.ConvertTokenX)
