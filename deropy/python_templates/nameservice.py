from deropy.dvm.functions import exists, store, load, strlen, signer, address_raw
from deropy.dvm.Smartcontract import SmartContract, logger, sc_logger


@sc_logger(logger)
class NameService(SmartContract):
    def Initialize(self) -> int:
        return 0

    def Register(self, name: str) -> int:
        if exists(name):
            return 0

        if strlen(name) >= 6:
            store(name, signer())
            return 0

        if signer() != address_raw("deto1qyvyeyzrcm2fzf6kyq7egkes2ufgny5xn77y6typhfx9s7w3mvyd5qqynr5hx"):
            return 0

    def TransferOwnership(self, name: str, new_owner: str) -> int:
        if load(name) != signer():
            return 1

        store(name, address_raw(new_owner))
        return 0
