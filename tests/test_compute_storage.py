import os
import importlib
import pytest

list_of_tests = {
    "AddressRaw": [
        {'args': {'address': '0x1234567890abcdef'}, 'expected': 0},
        {'args': {'address': '0x'}, 'expected': 0}],
    "AddressString": [
        {'args': {'address': '0x1234567890abcdef'}, 'expected': 0},
        {'args': {'address': '0x'}, 'expected': 0}],
    "AssetValue": [
        {'args': {'asset': '0x1234567890abcdef'}, 'expected': 0},
        {'args': {'asset': '0x'}, 'expected': 0}],
    "Atoi": [
        {'args': {'s': '1234'}, 'expected': 0},
        {'args': {'s': '1'}, 'expected': 0}],
    # "Blid": [{'args': {}, 'expected': 0}],
    "BlockHeight": [{'args': {}, 'expected': 0}],
    "BlockTimestamp": [{'args': {}, 'expected': 0}],
    "Delete": [{'args': {'key': 'variable_name'}, 'expected': 0}],
    "DeroValue": [{'args': {}, 'expected': 0}],
    "Dero": [{'args': {}, 'expected': 0}],
    "HexDecode": [{'args': {'s': '0x1234567890abcdef'}, 'expected': 0}],
    "Hex": [{'args': {'s': 0x1234567890abcdef}, 'expected': 0}],
    "IsAddressValid": [{'args': {'address': '0x1234567890abcdef'}, 'expected': 0}],
    "Itoa": [{'args': {'n': 1234}, 'expected': 0}],
    "Keccak256": [{'args': {'s': '0x1234567890abcdef'}, 'expected': 0}],
    "Store": [
        {'args': {'key': '5char', 'value': 'n'*5}, 'expected': 5},
        {'args': {'key': '50char', 'value': 'n'*50}, 'expected': 50}],
    "Load": [
        {'args': {'key': '5char'}, 'expected': 1},
        {'args': {'key': '50char'}, 'expected': 5}],
    "MapExists": [{'args': {'key': 'key'}, 'expected': 0}],
    "MapStore": [{'args': {'key': 'key', 'value': 'n'}, 'expected': 0}],
    "MapGet": [{'args': {'key': 'key'}, 'expected': 0}],
    "MapDelete": [{'args': {'key': 'key'}, 'expected': 0}],
    "Random": [{'args': {'value': 10}, 'expected': 0}],
    "UpdateScCode": [{'args': {'sc_code': 'this is the new code'}, 'expected': 20*2}],
    "SendDeroToAddress": [{'args': {'raw_address': '0x1234567890abcdef', 'amount': 100}, 'expected': 18}],
    "SendAssetToAddress": [{'args': {'raw_address': '0x1234567890abcdef', 'asset': '0x1234567890abcdef', 'amount': 100}, 'expected': 18*2}],
    "Signer": [{'args': {}, 'expected': 0}],
    "Sha256": [{'args': {'s': '0x1234567890abcdef'}, 'expected': 0}],
    "Sha3256": [{'args': {'s': '0x1234567890abcdef'}, 'expected': 0}],
    "Strlen": [{'args': {'s': '0x1234567890abcdef'}, 'expected': 0}],
    "Substr": [{'args': {'s': '0x1234567890abcdef', 'offset': 0, 'lenght': 5}, 'expected': 0}],

}
test_order = [
    "AddressRaw",
    "AddressString",
    "AssetValue",
    "Atoi",
    # "Blid",
    "BlockHeight",
    "BlockTimestamp",
    "Delete",
    "DeroValue",
    "Dero",
    "HexDecode",
    "Hex",
    "IsAddressValid",
    "Itoa",
    "Keccak256",
    "Store",
    "Load",
    "MapExists",
    "MapStore",
    "MapGet",
    "MapDelete",
    "Random",
    "UpdateScCode",
    "SendDeroToAddress",
    "SendAssetToAddress",
    "Signer",
    "Sha256",
    "Sha3256",
    "Strlen",
    "Substr",
]

# For each file, create a test case
@pytest.mark.parametrize('file', test_order)
def test_functions(file):
    module = importlib.import_module(f'deropy.dvm.functions.{file}')
    class_name = list(filter(lambda x: x != 'Function', dir(module)))[0]
    cls = getattr(module, class_name)
    func = cls()

    # Replace with actual arguments and expected result
    if class_name not in list_of_tests.keys():
        assert False

    # find all test for that class
    for test in list_of_tests[class_name]:
        args = test['args']
        expected = test['expected']
        func(**args)
        assert func.sc.gasStorage[-1] == expected