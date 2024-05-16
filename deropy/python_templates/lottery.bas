
Function Initialize() Uint64
1 IF exists("owner") != 0 THEN GOTO 8
2 store("owner", signer())
3 store("lotteryeveryXdeposit", 5)
4 store("lotterygiveback", 9900)
5 store("deposit_total", 0)
6 store("deposit_count", 0)
7 RETURN 0
8 RETURN 1
End Function

Function Lottery(val Uint64) Uint64
1 DIM deposit_count AS Uint64
2 LET deposit_count = load("deposit_count") + 1
3 IF val != 0 THEN GOTO 5
4 RETURN 0
5 IF val <= derovalue() THEN GOTO 7
6 RETURN 1
7 store("depositor_address" + deposit_count, signer())
8 store("deposit_total", load("deposit_total") + val)
9 store("deposit_count", deposit_count)
10 IF load("lotteryeveryXdeposit") < deposit_count THEN GOTO 12
11 RETURN 0
12 DIM winner AS Uint64
13 LET winner = random(deposit_count) + 1
14 send_dero_to_address(load("depositor_address" + winner), load("lotterygiveback") * load("deposit_total") / 10000)
15 store("deposit_total", 0)
16 store("deposit_count", 0)
17 RETURN 0
End Function

Function TuneLotteryParameters(lotteryeveryXdeposit Uint64, lotterygiveback Uint64) Uint64
1 IF load("owner") == signer() THEN GOTO 3
2 RETURN 1
3 store("lotteryeveryXdeposit", lotteryeveryXdeposit)
4 store("lotterygiveback", lotterygiveback)
5 RETURN 0
End Function

Function TransferOwnership(new_owner String) Uint64
1 IF load("owner") == signer() THEN GOTO 3
2 RETURN 1
3 store("tmpowner", address_raw(new_owner))
4 RETURN 0
End Function

Function ClaimOwnership() Uint64
1 IF load("tmpowner") == signer() THEN GOTO 3
2 RETURN 1
3 store("owner", signer())
4 RETURN 0
End Function

Function Withdraw(amount Uint64) Uint64
1 IF load("owner") == signer() THEN GOTO 3
2 RETURN 1
3 send_dero_to_address(signer(), amount)
4 RETURN 0
End Function

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
