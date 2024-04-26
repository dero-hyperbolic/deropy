from deropy.dvm.functions import store, load, signer, random, send_dero_to_address
from deropy.dvm.Smartcontract import SmartContract, logger, isPublic, sc_logger

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

if __name__ == '__main__':
    sc = Storage()
    sc.Initialize()
    sc.Lottery(1000)