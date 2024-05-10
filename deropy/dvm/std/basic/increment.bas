Function increment(k String, val Uint64) Uint64
1 STORE(key, LOAD(key) + val)
END Function