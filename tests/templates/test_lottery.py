from deropy.wallet.wallet_factory import WalletFactory
from deropy.dvm.tester import simulator_setup


# By default there is two global variables created by the simulator_setup fixture
# simulator: boolean that indicates if the tests are running in a simulator
# SmartContract: the class of the smart contract

# The function simulator_setup has to be called with a function that setups the wallets
# its role is to ensure that the wallets are associated with the simulator json_rpc endpoints to
# correspond to the wallets already created in the simulator


global simulator, SmartContract
simulator, SmartContract = simulator_setup('deropy.python_templates.lottery', 'Lottery')

wl_hyperbolic = WalletFactory.create_wallet('hyperbolic', simulator)
wl_new = WalletFactory.create_wallet('new_owner', simulator)
wl_random = WalletFactory.create_wallet('random_user', simulator)
sc = SmartContract()


class TestLottery:
    def test_initialize(self):
        wl_hyperbolic.invoke_sc_function(sc.Initialize)
        storage = sc.read()
        assert storage['deposit_count'] == 0
        assert storage['deposit_total'] == 0
        assert storage['owner'] == wl_hyperbolic.raw_address
        assert storage['lotteryeveryXdeposit'] == 5
        assert storage['lotterygiveback'] == 9900

    def test_initialize_cant_be_called_twice(self):
        wl_random.invoke_sc_function(sc.Initialize)
        storage = sc.read()
        assert storage['owner'] == wl_hyperbolic.raw_address

    def test_lottery_not_enough_deposit(self):
        wl_hyperbolic.invoke_sc_function(sc.Lottery, 1000)
        storage = sc.read()
        assert storage['deposit_count'] == 0
        assert storage['deposit_total'] == 0
        assert 'depositor_address1' not in storage

    def test_lottery_enough_deposit(self):
        wl_hyperbolic.invoke_sc_function(sc.Lottery, 1000, dero_deposit=1000)
        storage = sc.read()
        assert storage['deposit_count'] == 1
        assert storage['deposit_total'] == 1000
        assert storage['depositor_address1'] == wl_hyperbolic.raw_address

    def test_tune_owner(self):
        wl_hyperbolic.invoke_sc_function(sc.TuneLotteryParameters, (10, 9000))
        storage = sc.read()
        assert storage['lotteryeveryXdeposit'] == 10
        assert storage['lotterygiveback'] == 9000

    def test_tune_non_owner(self):
        wl_random.invoke_sc_function(sc.TuneLotteryParameters, (2, 9900))
        storage = sc.read()
        assert storage['lotteryeveryXdeposit'] == 10
        assert storage['lotterygiveback'] == 9000

    def test_transfer_ownership(self):
        wl_hyperbolic.invoke_sc_function(sc.TransferOwnership, wl_new.string_address)
        storage = sc.read()
        assert storage['tmpowner'] == wl_new.raw_address

    def test_claim_ownership_random(self):
        wl_random.invoke_sc_function(sc.ClaimOwnership)
        storage = sc.read()
        assert storage['owner'] != wl_random.raw_address
        assert storage['owner'] == wl_hyperbolic.raw_address

    def test_claim_ownership(self):
        wl_new.invoke_sc_function(sc.ClaimOwnership)
        storage = sc.read()
        assert storage['owner'] == wl_new.raw_address

    def test_withdraw_random(self):
        wl_random.invoke_sc_function(sc.Withdraw, 1000)
        storage = sc.read()
        assert storage['deposit_total'] == 1000

    def test_withdraw(self):
        wl_new.invoke_sc_function(sc.Withdraw, 1000)
