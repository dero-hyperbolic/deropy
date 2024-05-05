from deropy.dvm.functions import store, load, signer, exists, update_sc_code
from deropy.dvm.Smartcontract import SmartContract, logger, sc_logger
from deropy.dvm.Wallet import WalletSimulator, Wallet


@sc_logger(logger)
class Minimal(SmartContract):

    def Initialize(self) -> int:
        if exists("owner") == 0:
            store("owner", signer())
            store("original_owner", 0)
        else:
            return 1

    def UpdateSC(self, new_code: str) -> int:
        if signer() != load("owner"):
            return 1

        update_sc_code(new_code)
        return 0


if __name__ == '__main__':
    wl_hyperblic: Wallet = WalletSimulator.create_wallet('hyperbolic')

    sc = Minimal()
    wl_hyperblic.invoke_sc_function(sc.Initialize)
    wl_hyperblic.invoke_sc_function(sc.UpdateSC, "new_code")
