import pytest
from deropy.wallet.wallet_factory import WalletFactory
from deropy.dvm.tester import simulator_setup, clean_simulator


@pytest.fixture(scope='class', autouse=True)
def initialize_test_suite():
    global simulator, sc, SmartContract, wl_hyperbolic, wl_bisounours, wl_user1, wl_user2

    simulator, SmartContract = simulator_setup('deropy.python_templates.lottery', 'Lottery')
    wl_hyperbolic = WalletFactory.create_wallet('hyperbolic', simulator)
    wl_bisounours = WalletFactory.create_wallet('bisounours', simulator)
    wl_user1 = WalletFactory.create_wallet('wallet_user1', simulator)
    wl_user2 = WalletFactory.create_wallet('wallet_user2', simulator)
    sc = SmartContract()

    yield 

    clean_simulator()


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
        wl_user1.invoke_sc_function(sc.Initialize)
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
        wl_user1.invoke_sc_function(sc.TuneLotteryParameters, (2, 9900))
        storage = sc.read()
        assert storage['lotteryeveryXdeposit'] == 10
        assert storage['lotterygiveback'] == 9000

    def test_transfer_ownership(self):
        wl_hyperbolic.invoke_sc_function(sc.TransferOwnership, wl_user2.string_address)
        storage = sc.read()
        assert storage['tmpowner'] == wl_user2.raw_address

    def test_claim_ownership_random(self):
        wl_user1.invoke_sc_function(sc.ClaimOwnership)
        storage = sc.read()
        assert storage['owner'] != wl_user1.raw_address
        assert storage['owner'] == wl_hyperbolic.raw_address

    def test_claim_ownership(self):
        wl_user2.invoke_sc_function(sc.ClaimOwnership)
        storage = sc.read()
        assert storage['owner'] == wl_user2.raw_address

    def test_withdraw_random(self):
        wl_user1.invoke_sc_function(sc.Withdraw, 1000)
        storage = sc.read()
        assert storage['deposit_total'] == 1000

    def test_withdraw(self):
        wl_user2.invoke_sc_function(sc.Withdraw, 1000)
