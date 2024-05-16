from deropy.dvm.functions import load, signer, store, exists, strlen, update_sc_code


def updateCode(newCode: str):
    if load('owner') != signer():
        return 1

    # To apply the new code, newCode parameter must be empty
    if strlen(newCode) == 0:
        if strlen(load("nCode")) == 0:
            return 0
        else:
            update_sc_code(load("nCode"))
            store("nCode", "")
            return 0

    # To reset the variable, newCode parameter must be 1 character long
    if strlen(newCode) == 1:
        store("nCode", "")
        return 0

    # Update of create the nCode variable with the content of newCode parameter
    if exists("nCode") == 1:
        store("nCode", load("nCode") + "\n" + newCode)
        return 0
    
    store("nCode", newCode)
    return 0
