from deropy.dvm.Smartcontract import SmartContract
from deropy.dvm.Wallet import WalletSimulator, Wallet
from deropy.python_templates.minimum_sc import Minimal

# Let define three wallets
wl_hyperbolic: Wallet = WalletSimulator.create_wallet('hyperbolic')
wl_new: Wallet = WalletSimulator.create_wallet('new_owner')
wl_random: Wallet = WalletSimulator.create_wallet('random_user')

sc = Minimal()


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