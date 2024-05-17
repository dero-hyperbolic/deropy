from deropy.dvm.Smartcontract import SmartContract, logger, sc_logger

# Every DVM-BASIC function are simulated and can be imported from `deropy.dvn.functions` module.
from deropy.dvm.functions import store, signer, exists

# The standard library module contains function that are already implemented. By simply importing them, they will be
# available in the smart contract.
from deropy.dvm.std import updateCode


@sc_logger(logger)
class {{smartcontract_class}}(SmartContract):
    """
    This docstring bloc will appear as a comment header in your smart-contract.
    Be creative!

    {{project_name}} is developed using Deropy!
    """
    def Initialize(self) -> int:
        print(exists("owner"))
        if exists("owner") == 0:
            store("owner", signer())
            return 0
        else:
            return 1