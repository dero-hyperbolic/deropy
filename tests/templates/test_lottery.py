from deropy.wallet.wallet_factory import WalletFactory
from deropy.wallet.wallet import Wallet
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
simulator, SmartContract = simulator_setup('deropy.python_templates.lottery', 'Lottery')
wl_hyperbolic: Wallet = WalletFactory.create_wallet('hyperbolic', simulator)
wl_new: Wallet = WalletFactory.create_wallet('new_owner', simulator)
wl_random: Wallet = WalletFactory.create_wallet('random_user', simulator)
sc = SmartContract()


class TestLottery:
    def test_initialize(self):
        wl_hyperbolic.invoke_sc_function(sc.Initialize)
        current_storage = sc.read()
        assert current_storage['deposit_count'] == 0
        assert current_storage['deposit_total'] == 0
        assert current_storage['owner'] == wl_hyperbolic.raw_address
        assert current_storage['lotteryeveryXdeposit'] == 5
        assert current_storage['lotterygiveback'] == 9900

    def test_initialize_cant_be_called_twice(self):
        wl_random.invoke_sc_function(sc.Initialize)
        current_storage = sc.read()
        assert current_storage['owner'] == wl_hyperbolic.raw_address

    def test_lottery_not_enough_deposit(self):
        wl_hyperbolic.invoke_sc_function(sc.Lottery, 1000)
        current_storage = sc.read()
        assert current_storage['deposit_count'] == 0
        assert current_storage['deposit_total'] == 0
        assert 'depositor_address1' not in current_storage

    def test_lottery_enough_deposit(self):
        wl_hyperbolic.invoke_sc_function(sc.Lottery, 1000, dero_deposit=1000)
        current_storage = sc.read()
        assert current_storage['deposit_count'] == 1
        assert current_storage['deposit_total'] == 1000
        assert current_storage['depositor_address1'] == wl_hyperbolic.raw_address

    def test_tune_owner(self):
        wl_hyperbolic.invoke_sc_function(sc.TuneLotteryParameters, (10, 9000))
        current_storage = sc.read()
        assert current_storage['lotteryeveryXdeposit'] == 10
        assert current_storage['lotterygiveback'] == 9000

    def test_tune_non_owner(self):
        wl_random.invoke_sc_function(sc.TuneLotteryParameters, (2, 9900))
        current_storage = sc.read()
        assert current_storage['lotteryeveryXdeposit'] == 10
        assert current_storage['lotterygiveback'] == 9000

    def test_transfer_ownership(self):
        wl_hyperbolic.invoke_sc_function(sc.TransferOwnership, wl_new.string_address)
        current_storage = sc.read()
        assert current_storage['tmpowner'] == wl_new.raw_address

    def test_claim_ownership_random(self):
        wl_random.invoke_sc_function(sc.ClaimOwnership)
        current_storage = sc.read()
        assert current_storage['owner'] != wl_random.raw_address
        assert current_storage['owner'] == wl_hyperbolic.raw_address

    def test_claim_ownership(self):
        wl_new.invoke_sc_function(sc.ClaimOwnership)
        current_storage = sc.read()
        assert current_storage['owner'] == wl_new.raw_address

    def test_withdraw_random(self):
        wl_random.invoke_sc_function(sc.Withdraw, 1000)
        current_storage = sc.read()
        assert current_storage['deposit_total'] == 1000

    def test_withdraw(self):
        wl_new.invoke_sc_function(sc.Withdraw, 1000)
