from deropy.dvm.functions import exists, store, load, dero_value, asset_value, signer, address_raw, send_dero_to_address
from deropy.dvm.functions import send_asset_to_address, scid
from deropy.dvm.Smartcontract import SmartContract, logger, sc_logger


@sc_logger(logger)
class Token(SmartContract):
    def InitializePrivate(self) -> int:
        if exists("owner") == 0:
            store("owner", signer())
            send_asset_to_address(signer(), 1000, scid())
            return 0
        else:
            return 1

    def IssueTokenX(self) -> int:
        send_asset_to_address(signer(), dero_value(), scid())
        return 0

    def ConvertTokenX(self) -> int:
        send_dero_to_address(signer(), asset_value(scid()))
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

