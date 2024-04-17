Function Initialize() Uint64
1 IF EXISTS("owner") THEN GOTO 10
2 STORE("owner", SIGNER())
3 STORE("original_owner", 0)
10 RETURN 0
End Function

Function UpdateCode(code String) Uint64
1 IF LOAD("owner") != SIGNER() THEN GOTO 11
2 UPDATE_SC_CODE(code)
3 RETURN 0
11 RETURN 1
End Function

// Function AppendCode(code String) Uint64
// 1 IF LOAD("owner") != SIGNER() THEN GOTO 11
// 2 APPEND_SC_CODE(code)
// 3 RETURN 0
// 11 RETURN 1
// End Function