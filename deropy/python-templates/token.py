from deropy.dvm.functions import store, load, dero_value, asset_value, signer, address_raw, send_dero_to_address
from deropy.dvm.functions import send_asset_to_address, scid
from deropy.dvm.Smartcontract import SmartContract, logger, sc_logger


@sc_logger(logger)
class Token(SmartContract):
    def InitializePrivate(self) -> int:
        store("owner", signer())
        send_asset_to_address(signer(), 1000, scid())
        return 0

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


# We can now test the smart contract by creating a scenario.
# For more complexe SC, it will be necessary to create a proper test suite.
if __name__ == '__main__':
    from deropy.dvm.Wallet import WalletSimulator

    # Let define three wallets
    WalletSimulator.create_wallet('hyperbolic')
    WalletSimulator.create_wallet('new_owner')
    WalletSimulator.create_wallet('random_user')

    WalletSimulator.active_wallet = 'hyperbolic'
    sc = Token()

    # Initialize the smart contract (akin to deployement on the blockchain)
    sc.InitializePrivate()

    # Test the IssueTokenX function
    sc.send_dero_with_tx(100)
    assert sc.IssueTokenX() == 0

    # Test the ConvertTokenX function
    assert sc.ConvertTokenX() == 0
