from deropy.dvm.functions import store, load


def decrement(self, key: str, amount: int) -> int:
    store(key, load(key) - amount)
    return 0