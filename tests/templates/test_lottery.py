from deropy.dvm.Smartcontract import SmartContract
from deropy.dvm.Wallet import WalletSimulator, Wallet
from deropy.python_templates.lottery import Lottery

# Configure the test scenario
wl_hyperbolic: Wallet = WalletSimulator.create_wallet('hyperbolic')
wl_new: Wallet = WalletSimulator.create_wallet('new_owner')
wl_random: Wallet = WalletSimulator.create_wallet('random_user')

sc = Lottery()


class TestLottery:
    def test_initialize(self):
        wl_hyperbolic.invoke_sc_function(sc.Initialize)
        current_storage = SmartContract.get_instance().storage
        assert current_storage['deposit_count'] == 0
        assert current_storage['deposit_total'] == 0
        assert current_storage['owner'] == wl_hyperbolic.raw_address
        assert current_storage['lotteryeveryXdeposit'] == 2
        assert current_storage['lotterygiveback'] == 9900

    def test_initialize_cant_be_called_twice(self):
        wl_random.invoke_sc_function(sc.Initialize)
        current_storage = SmartContract.get_instance().storage
        assert current_storage['owner'] == wl_hyperbolic.raw_address

    def test_lottery(self):
        wl_hyperbolic.invoke_sc_function(sc.Lottery, 1000)
        current_storage = SmartContract.get_instance().storage
        assert current_storage['deposit_count'] == 1
        assert current_storage['deposit_total'] == 1000
        assert current_storage['depositor_address0']
        assert current_storage['depositor_address0'] == wl_hyperbolic.raw_address

    def test_tune_owner(self):
        wl_hyperbolic.invoke_sc_function(sc.TuneLotteryParameters, (10, 9000))
        current_storage = SmartContract.get_instance().storage
        assert current_storage['lotteryeveryXdeposit'] == 10
        assert current_storage['lotterygiveback'] == 9000

    def test_tune_non_owner(self):
        wl_random.invoke_sc_function(sc.TuneLotteryParameters, (2, 9900))
        current_storage = SmartContract.get_instance().storage
        assert current_storage['lotteryeveryXdeposit'] == 10
        assert current_storage['lotterygiveback'] == 9000

    def test_transfer_ownership(self):
        wl_hyperbolic.invoke_sc_function(sc.TransferOwnership, wl_new.string_address)
        current_storage = SmartContract.get_instance().storage
        assert current_storage['tmpowner'] == wl_new.raw_address

    def test_claim_ownership_random(self):
        wl_random.invoke_sc_function(sc.ClaimOwnership)
        current_storage = SmartContract.get_instance().storage
        assert current_storage['owner'] != wl_random.raw_address
        assert current_storage['owner'] == wl_hyperbolic.raw_address

    def test_claim_ownership(self):
        wl_new.invoke_sc_function(sc.ClaimOwnership)
        current_storage = SmartContract.get_instance().storage
        assert current_storage['owner'] == wl_new.raw_address

    def test_withdraw_random(self):
        wl_random.invoke_sc_function(sc.Withdraw, 1000)
        current_storage = SmartContract.get_instance().storage
        assert current_storage['deposit_total'] == 1000

    def test_withdraw(self):
        wl_new.invoke_sc_function(sc.Withdraw, 1000)
        current_storage = SmartContract.get_instance().storage
