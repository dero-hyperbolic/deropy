Function UpdateCode(newCode String) Uint64
1 IF LOAD("owner") != SIGNER() THEN GOTO 101
2 IF STRLEN(newCode) == 0 THEN GOTO 10
3 IF STRLEN(newCode) == 1 THEN GOTO 20
4 IF EXISTS("nCode") == 1 THEN GOTO 7
5 STORE("nCode", newCode)
6 GOTO 100
7 STORE("nCode", LOAD("nCode") + "\n" + newCode)
8 GOTO 100
10 UPDATE_SC_CODE(LOAD("nCode"))
11 STORE("nCode", "")
12 GOTO 100
20 STORE("nCode", "")
100 RETURN 0
101 RETURN 1
End Function