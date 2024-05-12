from deropy.dvm.functions import load, signer, store, exists, strlen, update_sc_code


def updateCode(newCode: str):
    if load('owner') != signer():
        return 1

    if strlen(newCode) == 0:
        update_sc_code(load("nCode"))
        store("nCode", "")
        return 0

    if exists("nCode") == 1:
        store("nCode", load("nCode") + "\n" + newCode)
    else:
        store("nCode", newCode)
    return 0
