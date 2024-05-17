from deropy.dvm.functions import load, signer, store, address_raw


def TransferOwnership(str_address: str) -> int:
    if load('owner') != signer():
        return 1

    store('newOwner', address_raw(str_address))
    return 0
