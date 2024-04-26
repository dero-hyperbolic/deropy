import pprint

from deropy.dvm.functions import store, load, signer, random, send_dero_to_address, address_raw, update_sc_code
from deropy.dvm.Smartcontract import SmartContract, logger, isPublic, sc_logger
from deropy.dvm.utils import get_address, get_raw_address

@sc_logger(logger)
class Storage(SmartContract):

    def Initialize(self) -> int:
        store('owner', signer())
        store('lotteryeveryXdeposit', 2)
        store('lotterygiveback', 9900)
        store('deposit_total', 0)
        store('deposit_count', 0)
        return 0

    def Lottery(self, value: int) -> int:
        deposit_count: int = load("deposit_count") + 1
        if value == 0:
            return 0
        store('depositor_address' + str(deposit_count - 1), signer())
        store('deposit_total', load('deposit_total') + value)
        store('deposit_count', deposit_count)
        
        if load('lotteryeveryXdeposit') > deposit_count:
            return 0
        
        winner: int = random(0, deposit_count)
        send_dero_to_address(load('depositor_address' + str(winner)), load('lotterygiveback')*load("deposit_total")/10000)
        store('deposit_total', 0)
        store('deposit_count', 0)
        return 0
    
    def TuneLotteryParameters(self, lotteryeveryXdeposit: int, lotterygiveback: int) -> int:
        if load('owner') != signer():
            return 1
        
        store('lotteryeveryXdeposit', lotteryeveryXdeposit)
        store('lotterygiveback', lotterygiveback)
        return 0
    
    def TransferOwnership(self, new_owner: str) -> int:
        if load('owner') != signer():
            return 1
        
        store('tmpowner', address_raw(new_owner))
        return 0
    
    def ClaimOwnership(self) -> int:
        if load('tmpowner') != signer():
            return 1
        
        store('owner', signer())
        return 0
    
    def Withdraw(self, amount: int) -> int:
        if load('owner') != signer():
            return 1
        
        send_dero_to_address(signer(), amount)
        return 0
    
    def UpdateCode(self, new_code: str) -> int:
        if load('owner') != signer():
            return 1
        
        update_sc_code(new_code)
        return 0



# We can now test the smart contract by creating a scenario.
# For more complexe SC, it will be necessary to create a proper test suite.
if __name__ == '__main__':
    original_signer = 'hyperbolic'
    new_owner = 1
    random_user = 2

    # configure the test scenario
    SmartContract.active_wallet = get_address(original_signer)
    sc = Storage()

    # Initialize the smart contract (akin to deployement on the blockchain)
    sc.Initialize()
    current_storage = SmartContract.get_instance().storage
    assert current_storage['deposit_count'] == 0
    assert current_storage['deposit_total'] == 0
    assert current_storage['owner'] == get_raw_address(original_signer)
    assert current_storage['lotteryeveryXdeposit'] == 2
    assert current_storage['lotterygiveback'] == 9900

    # Play the lottery
    sc.Lottery(1000)
    current_storage = SmartContract.get_instance().storage
    assert current_storage['deposit_count'] == 1
    assert current_storage['deposit_total'] == 1000
    assert current_storage['depositor_address0']
    assert current_storage['depositor_address0'] == get_raw_address(original_signer)

    # The owner tune the lottery parameters
    sc.TuneLotteryParameters(10, 9000)
    current_storage = SmartContract.get_instance().storage
    assert current_storage['lotteryeveryXdeposit'] == 10
    assert current_storage['lotterygiveback'] == 9000

    # somebody else than the owner try to tune the lottery parameters
    SmartContract.active_wallet = get_address(random_user)
    sc.TuneLotteryParameters(2, 9900)
    current_storage = SmartContract.get_instance().storage
    assert current_storage['lotteryeveryXdeposit'] == 10
    assert current_storage['lotterygiveback'] == 9000

    # The owner transfer the ownership
    SmartContract.active_wallet = get_address(original_signer)
    sc.TransferOwnership(get_address(new_owner))
    current_storage = SmartContract.get_instance().storage
    assert current_storage['tmpowner'] == get_raw_address(new_owner)

    # Somebody random try to claim the ownership, it should not work
    SmartContract.active_wallet = get_address(random_user)
    sc.ClaimOwnership()
    current_storage = SmartContract.get_instance().storage
    assert current_storage['owner'] != get_raw_address(random_user)
    assert current_storage['owner'] == get_raw_address(original_signer)
    
    # The new owner claim the ownership
    SmartContract.active_wallet = get_address(new_owner)
    sc.ClaimOwnership()
    current_storage = SmartContract.get_instance().storage
    assert current_storage['owner'] == get_raw_address(new_owner)

    # Somebody random try to withdraw, it should not work
    SmartContract.active_wallet = get_address(random_user)
    sc.Withdraw(1000)
    current_storage = SmartContract.get_instance().storage
    assert current_storage['deposit_total'] == 1000

    # the owner withdraw
    SmartContract.active_wallet = get_address(new_owner)
    sc.Withdraw(1000)
    current_storage = SmartContract.get_instance().storage
