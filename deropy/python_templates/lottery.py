from deropy.dvm.functions import exists, store, load, signer, random, send_dero_to_address, address_raw, update_sc_code
from deropy.dvm.Smartcontract import SmartContract, logger, sc_logger


@sc_logger(logger)
class Lottery(SmartContract):
    def Initialize(self) -> int:
        if exists('owner') == 0:
            store('owner', signer())
            store('lotteryeveryXdeposit', 5)
            store('lotterygiveback', 9900)
            store('deposit_total', 0)
            store('deposit_count', 0)
            return 0
        return 1

    def Lottery(self, val: int) -> int:
        deposit_count: int = load("deposit_count") + 1
        if val == 0:
            return 0
        store('depositor_address' + str(deposit_count), signer())
        store('deposit_total', load('deposit_total') + val)
        store('deposit_count', deposit_count)

        if load('lotteryeveryXdeposit') >= deposit_count:
            return 0

        winner: int = random(deposit_count) + 1
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
