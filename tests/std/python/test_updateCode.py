import pytest


from deropy.dvm.functions import store, signer
from deropy.dvm.std import updateCode
from deropy.dvm.Smartcontract import SmartContract
from deropy.wallet.wallet_factory import WalletFactory


# Wrap the function into a basic smart contract to can simulate the execution
class UpdateCodeSC(SmartContract):
    def Initialize(self) -> int:
        store("owner", signer())
        return 0
    
    def updateCode(self, new_code: str) -> int:
        return updateCode(new_code)
    

@pytest.fixture(scope="class", autouse=True)
def initialize_test_suite():
    global sc, wl_hyperbolic, wl_user1

    wl_hyperbolic = WalletFactory.create_wallet("hyperbolic", simulator=False)
    wl_user1 = WalletFactory.create_wallet("wallet_user1", simulator=False)
    sc = UpdateCodeSC()


class TestUpdateCodeSC:
    def test_initialize(self):
        wl_hyperbolic.invoke_sc_function(sc.Initialize)

    def test_update_code_when_not_owner(self):
        wl_user1.invoke_sc_function(sc.updateCode, "new_code")
        storage = sc.read()
        assert "nCode" not in storage

    def test_update_code_when_owner(self):
        wl_hyperbolic.invoke_sc_function(sc.updateCode, "new_code")
        storage = sc.read()
        assert "nCode" in storage
        assert storage["nCode"] == "new_code"

    def test_append_code_when_owner(self):
        wl_hyperbolic.invoke_sc_function(sc.updateCode, "appended_code")
        storage = sc.read()
        assert "nCode" in storage
        assert storage["nCode"] == "new_code\nappended_code"

    def test_variable_is_reset_if_parameter_length_is_one(self):
        wl_hyperbolic.invoke_sc_function(sc.updateCode, "a")
        storage = sc.read()
        assert storage["nCode"] == ""

    def test_update_code_when_owner_2(self):
        wl_hyperbolic.invoke_sc_function(sc.updateCode, "new_code")
        storage = sc.read()
        assert "nCode" in storage
        assert storage["nCode"] == "\nnew_code"

    def test_code_is_changed_when_parameter_length_is_zero(self):
        wl_hyperbolic.invoke_sc_function(sc.updateCode, "")
        storage = sc.read()
        assert storage["nCode"] == ""