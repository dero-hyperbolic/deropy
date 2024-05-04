import pytest

from deropy.dvm.functions import store, load, exists, delete
from deropy.dvm.Smartcontract import SmartContract


class TestMapStore:
    def test_store_string(self):
        store('key', 'value')

        sc = SmartContract.get_instance()
        assert sc.storage['key'] == 'value'

    def test_store_empty_string(self):
        store('key', '')

        sc = SmartContract.get_instance()
        assert sc.storage['key'] == ''

    def test_store_int(self):
        store('key', 1)

        sc = SmartContract.get_instance()
        assert sc.storage['key'] == 1


class TestMapGet:
    def test_get_string(self):
        store('key', 'value')

        assert load('key') == 'value'

    def test_get_empty_string(self):
        store('key', '')

        assert load('key') == ''

    def test_get_int(self):
        store('key', 1)

        assert load('key') == 1

    def test_get_non_existent_key(self):
        with pytest.raises(KeyError):
            load('not_a_key_in_memory')


class TestMapDelete:
    def test_delete_string(self):
        store('key', 'value')
        delete('key')

        with pytest.raises(KeyError):
            load('key')


class TestMapExists:
    def test_exists(self):
        store('key', 'value')

        assert exists('key') == 1
