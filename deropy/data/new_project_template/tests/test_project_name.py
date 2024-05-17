import pytest
from deropy.wallet.wallet_factory import WalletFactory
from deropy.dvm.tester import simulator_setup, clean_simulator


# The following fixture is used to initialize the test suite
# it ensure that the different wallets and the smart contract are created
# and can be use during the simulation
@pytest.fixture(scope='class', autouse=True)
def initialize_test_suite():
    global simulator, sc, SmartContract, wl_hyperbolic, wl_bisounours, wl_user1, wl_user2

    # A bit of context:
    # When running on the python simulator, we simply need the smart-contract class and directly executes its function
    # But when running on the derohe simulator, we need to send json-rpc request to the simulator in order to interact with the SC
    # The following line will return the correct class (pure python SC, or generated SC for the derohe simulator)
    simulator, SmartContract = simulator_setup('src.{{project_name}}', '{{smartcontract_class}}')

    wl_hyperbolic = WalletFactory.create_wallet('hyperbolic', simulator)
    wl_user1 = WalletFactory.create_wallet('wallet_user1', simulator)
    sc = SmartContract()

    yield 

    clean_simulator()


class Test{{smartcontract_class}}:
    def test_initialize(self):
        # If running in the python simulator, calling the Initialize function is equivalent to installing the SC
        if not simulator:
            wl_hyperbolic.invoke_sc_function(sc.Initialize)
            storage = sc.read()
            assert storage['owner'] == wl_hyperbolic.raw_address

        # When in the DEROHE simulator, the SC is already installed
        else:
            assert True

    def test_other(self):
        assert True