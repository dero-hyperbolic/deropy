import pytest
from deropy.wallet.wallet_factory import WalletFactory
from deropy.dvm.tester import simulator_setup, clean_simulator


@pytest.fixture(scope='class', autouse=True)
def initialize_test_suite():
    global simulator, sc, SmartContract, wl_hyperbolic, wl_random

    simulator, SmartContract = simulator_setup('deropy.python_templates.minimun_sc', 'Minimal')
    wl_hyperbolic = WalletFactory.create_wallet('hyperbolic', simulator)
    wl_random = WalletFactory.create_wallet('random', simulator)
    sc = SmartContract()

    yield 

    clean_simulator()


class TestMinimumSC:
    def test_inialized(self):
        wl_hyperbolic.invoke_sc_function(sc.Initialize)
        current_storage = SmartContract.get_instance().storage
        assert current_storage['owner'] == wl_hyperbolic.raw_address
        assert current_storage['original_owner'] == wl_hyperbolic.raw_address