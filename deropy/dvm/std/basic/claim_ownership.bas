Function ClaimOwnership() Uint64
1 IF LOAD("newOwner") != SIGNER() THEN GOTO 11
2 STORE("owner", SIGNER())
10 RETURN 0
11 RETURN 1
End Function