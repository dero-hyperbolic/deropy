Function UpdateCode(newCode String) Uint64
1 IF LOAD("owner") != SIGNER() THEN GOTO 101
2 IF STRLEN(newCode) == 0 THEN GOTO 10
3 STORE("nCode", LOAD("nCode") + "\n" + newCode)
4 GOTO 100
10 UPDATE_SC_CODE(LOAD("nCode"))
11 STORE("nCode", "")
100 RETURN 0
101 RETURN 1
End Function