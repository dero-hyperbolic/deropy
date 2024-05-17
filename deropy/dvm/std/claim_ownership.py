from deropy.dvm.functions import load, signer, store


def ClaimOwnership() -> int:
    if load('newOwner') != signer():
        return 1

    store("owner", signer())
    return 0