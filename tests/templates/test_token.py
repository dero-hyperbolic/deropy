import pytest
from deropy.wallet.wallet_factory import WalletFactory
from deropy.dvm.tester import simulator_setup, clean_simulator


@pytest.fixture(scope='class', autouse=True)
def initialize_test_suite():
    global simulator, sc, SmartContract, wl_hyperbolic, wl_user1

    simulator, SmartContract = simulator_setup('deropy.python_templates.token', 'Token')
    wl_hyperbolic = WalletFactory.create_wallet('hyperbolic', simulator)
    wl_user1 = WalletFactory.create_wallet('wallet_user1', simulator)
    sc = SmartContract()

    yield 

    clean_simulator()


class TestNameService:
    def test_inialized(self):
        wl_hyperbolic.invoke_sc_function(sc.InitializePrivate)
        storage = sc.read()
        assert storage['owner'] == wl_hyperbolic.raw_address

    def test_initialize_cant_be_called_twice(self):
        wl_user1.invoke_sc_function(sc.InitializePrivate)
        storage = sc.read()
        assert storage['owner'] == wl_hyperbolic.raw_address

    def test_issue_token(self):
        wl_hyperbolic.invoke_sc_function(sc.IssueTokenX, dero_deposit=100)

    def test_convert_token(self):
        wl_hyperbolic.invoke_sc_function(sc.ConvertTokenX)
