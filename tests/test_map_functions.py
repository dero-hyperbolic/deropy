import pytest

from deropy.dvm.functions import map_store, map_get, map_delete, map_exists
from deropy.dvm.Smartcontract import SmartContract


class TestMapStore:
    def test_store_string(self):
        map_store('key', 'value')

        sc = SmartContract.get_instance()
        assert sc.memory['key'] == 'value'

    def test_store_empty_string(self):
        map_store('key', '')

        sc = SmartContract.get_instance()
        assert sc.memory['key'] == ''

    def test_store_int(self):
        map_store('key', 1)

        sc = SmartContract.get_instance()
        assert sc.memory['key'] == 1


class TestMapGet:
    def test_get_string(self):
        map_store('key', 'value')

        assert map_get('key') == 'value'

    def test_get_empty_string(self):
        map_store('key', '')

        assert map_get('key') == ''

    def test_get_int(self):
        map_store('key', 1)

        assert map_get('key') == 1

    def test_get_non_existent_key(self):
        with pytest.raises(KeyError):
            map_get('not_a_key_in_memory')


class TestMapDelete:
    def test_delete_string(self):
        map_store('key', 'value')
        map_delete('key')

        print(SmartContract.get_instance().memory)

        with pytest.raises(KeyError):
            map_get('key')


class TestMapExists:
    def test_exists(self):
        map_store('key', 'value')

        assert map_exists('key') == 1
