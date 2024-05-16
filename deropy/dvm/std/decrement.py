from deropy.dvm.functions import store, load


def decrement(key: str, val: int) -> int:
    store(key, load(key) - val)
    return 0
