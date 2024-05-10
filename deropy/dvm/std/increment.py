from deropy.dvm.functions import store, load


def increment(self, key: str, amount: int) -> int:
    store(key, load(key) + amount)
    return 0