from deropy.wallet.wallet_factory import WalletFactory
from deropy.dvm.tester import simulator_setup


simulator, SmartContractClass = simulator_setup('deropy.python_templates.token', 'Token')
wl_hyperbolic = WalletFactory.create_wallet('hyperbolic', simulator)
wl_random = WalletFactory.create_wallet('random_user', simulator)
sc = SmartContractClass()


class TestNameService:
    def test_inialized(self):
        wl_hyperbolic.invoke_sc_function(sc.InitializePrivate)
        storage = sc.read()
        assert storage['owner'] == wl_hyperbolic.raw_address

    def test_initialize_cant_be_called_twice(self):
        wl_random.invoke_sc_function(sc.InitializePrivate)
        storage = sc.read()
        assert storage['owner'] == wl_hyperbolic.raw_address

    def test_issue_token(self):
        wl_hyperbolic.invoke_sc_function(sc.IssueTokenX, dero_deposit=100)

    def test_convert_token(self):
        wl_hyperbolic.invoke_sc_function(sc.ConvertTokenX)
