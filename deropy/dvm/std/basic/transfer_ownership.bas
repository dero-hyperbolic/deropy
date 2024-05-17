Function TransferOwnership(str_addr String) Uint64
1 IF LOAD("owner") != SIGNER() THEN GOTO 11
2 STORE("newOwner", ADDRES_RAW(str_addr))
10 RETURN 0
11 RETURN 1
End Function