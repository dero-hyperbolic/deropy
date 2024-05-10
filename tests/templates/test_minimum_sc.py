from deropy.wallet.wallet_factory import WalletFactory
from deropy.wallet.wallet import Wallet
from deropy.dvm.tester import simulator_setup


simulator, SmartContract = simulator_setup('deropy.python_templates.minimum_sc', 'Minimal')
wl_hyperbolic: Wallet = WalletFactory.create_wallet('hyperbolic')
wl_new: Wallet = WalletFactory.create_wallet('new_owner')
wl_random: Wallet = WalletFactory.create_wallet('random_user')

sc = SmartContract()


class TestMinimumSC:
    def test_inialized(self):
        wl_hyperbolic.invoke_sc_function(sc.Initialize)
        current_storage = SmartContract.get_instance().storage
        assert current_storage['owner'] == wl_hyperbolic.raw_address
        assert current_storage['original_owner'] == wl_hyperbolic.raw_address

    def test_initialize_cant_be_called_twice(self):
        wl_random.invoke_sc_function(sc.Initialize)
        current_storage = SmartContract.get_instance().storage
        assert current_storage['owner'] == wl_hyperbolic.raw_address