from deropy.dvm.Smartcontract import SmartContract
from deropy.dvm.Wallet import WalletSimulator, Wallet
from deropy.python_templates.token import Token

# Let define three wallets
wl_hyperbolic: Wallet = WalletSimulator.create_wallet('hyperbolic')
wl_random: Wallet = WalletSimulator.create_wallet('random_user')

# configure the test scenario
SmartContract.get_instance().reset_sc()
sc = Token()


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
