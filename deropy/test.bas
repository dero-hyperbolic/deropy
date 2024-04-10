Function Initialize() Uint64
1 IF EXISTS("original_owner") == 1 THEN GOTO 10
2 RETURN 1
3 STORE("owner", SIGNER())
4 STORE("orignal_owner", SIGNER())
// Each request, provider, and validators are unique and define by the sequence. A maximum a 2^32-1 (4294967295) or each. 
7 STORE("r_seq", 0) // request counter
10 RETURN 0
End Function

Function TransferOwnership(newOwner String) Uint64
1 IF LOAD("owner") != SIGNER() THEN GOTO 11
2 STORE("owner", ADDRESS_RAW(newOwner))
10 RETURN 0
11 RETURN 1
End Function

// Customer functions
// bounty is price in DERI, file_size is in bytes, duration is in seconds
Function RequestStorage(bounty Uint64, file_size Uint64, duration Uint64) Uint64
1 DIM k AS String
// TODO Verification -------------
// Minimum duration 86400 * 180 ~ 6 months
// Minimum Bounty
//    - Reward should be enough to guarantee validator are in benefit
//    - Validator can validate up to 2300 SR at the same time
//    - cost = 200 DERI
//    - Ponderate cost = 200 / 2300 = 0.08695652 DERI 
//      Impossible based on integer, --> use fixed point arithmetic
//      factor F = 1000
//      Everything related to DERI will be multiplied by 1000 during the computation
//      The final result will be divided by 10000
//      -> ponderate daily Fcost = 2000000 / 23000 = 830 FDERI
//    - total Fcost = 83 * duration (in days)
//    ---- COMPUTE Factored DAILY BOUNTY (F_DBv) FOR VALIDATOR
//    - Validator get 20% of the bounty 20% -> F_DBv/5
//    - There is 10 validator to reward each day -> F_DBv/10
//    - The bounty is split for all the duration -> F_DBv/duration
//    - F_DBv = F_Bounty / 5 / 10 / duration
//    - Bounty is valid only if the Minimum Daily Bounty is bigger that the ponderate cost
//    - Valid = F_DBv > 830
//    ---- COMPUTE Factored DAILY BOUNTY (F_DBp) FO R PROVIDER
//    - Providor get 80% of the bounty. 80% = /5*4
//    - There is 5 Providor. /5
//    - The bounty is split for all the duration. /duration
//    - F_DBp = F_Bounty / 5 * 4 / 5 / duration
//    ---- Example
//    - RequestStorage(200000, 20k, 365*86400) -> 2 Dero for 1 year
//    - F_DBv = 109589
//    - F_DBv > 830 --> Bounty is valid for rewarding validator
//    - F_DBp = 876712
//    - Convert to DERI
//    - DBv = 109589 / 10000 = 11 DERI
//    - DVp = 876712 / 10000 = 87 DERI
//    ---- Verification
//    - 365 * (109589*10 + 876712*5) = 1999999999 FDERI = 19999 DERI (99.999 %)
//    ---- COMPUTING MINIMUM BOUNTY TO ENSURE FAIR PAYMENT
//    - Example for 1 year, 365 days
//    - F_DBv > 830
//    - Each validator need to be rewarded at least 83 FDERI every day
//    - There is 10 validator -> 8300 FDERI
//    - 8300 * 365 = 3029500 FDERI
//    --> 3029500 FDERI for 1 year just 1514 the validator
//    --> 3029500 FDERI represent 20% of the bounty, total bounty is 5 times this
//    - 3029500 * 5 = 15147500 FDERI
//    --> Minimum of 15147500 / 10000 = 1515 DERI
2 DIM min As Uint64
3 LET min = 830 * 365 * 10 * 5 / 1000
4 IF bounty < min THEN GOTO 102 // Bounty too small to be fair

5 next("r_seq") // store in RAM the next uid for the request 
6 LET k = "RS_" + HEX8(LOAD("r_seq"))
7 now()
8 STORE(k + "_Bounty", bounty)
9 STORE(k + "_InitialBounty", bounty)
10 STORE(k + "_FileSize", file_size)
11 STORE(k + "_Duration", duration)
12 STORE(k + "_CreatedAt", MAPLOAD("t"))
13 STORE(k + "_IPFS_Ref", "")
14 STORE(k + "_ProviderCount", 5)
15 STORE(k + "_Providers", "")
16 STORE(k + "_ValidatorCout", 10)
17 STORE(k + "_Validators", "")
18 STORE(k + "_LastVerif", MAPLOAD("t"))
19 STORE(k + "_SizeVerif", 0)
// 17 STORE(k + p, 0)  Just to comment that this variables is created when a provider fullfill the request
// it is counter that is incremented when a provider DO NOT FULLFILL the request
// if it reaches 3, then the provider is slashed
100 RETURN 0
101 RETURN 1
102 RETURN 2
End Function

// Provider functions ------------------------------------------------------------------------
Function RegisterProvider(IPFS_CID String) Uint64
1 DIM k AS String // Create the unique identifier for the provider
2 LET k = "P_" + HEX(SHA256(SIGNER()))
3 IF EXISTS(k) == 1 THEN GOTO 11 // Provider already registered
4 STORE(k + "_IPFS_CID", IPFS_CID)
5 STORE(k + "_StorageCount", 0)
6 STORE(k + "_wallet", SIGNER())
7 STORE(k + "_Balance", 0)
10 RETURN 0
11 RETURN 1
End Function

Function UnregisterProvider() Uint64
1 DIM k AS String
2 LET k = "P_" + HEX(SHA256(SIGNER()))
3 IF EXISTS(k) == 0 THEN GOTO 11 // Provider not registered
4 IF LOAD(k + "_StorageCount") != 0 THEN GOTO 12 // Provider still has storage
5 DELETE(k)
6 DELETE(k + "_IPFS_CID")
7 DELETE(k + "_StorageCount")
8 DELETE(k + "_wallet")
9 DELETE(k + "_Balance")
// There is no need to remove the provider from the requests since the validators will
// take care of that
10 RETURN 0
11 RETURN 1
12 RETURN 2
End Function

Function WithdrawProvider() Uint64
1 DIM k AS String
2 LET k = "P_" + HEX(SHA256(SIGNER()))
3 RETURN withdraw(k)
End Function

Function FullfilStorage(RS_K String) Uint64
1 DIM k AS String
2 DIM rsk AS String
3 LET k = "P_" + HEX(SHA256(SIGNER()))
4 LET rsk = "RS_" + RS_K
5 IF EXISTS(k) == 0 THEN GOTO 101 // Provider not registered
6 IF EXISTS(rsk) == 0 THEN GOTO 102 // Request not found
7 IF LOAD(rsk + "_ProviderCount") == 0 THEN GOTO 103 // Request already fullfilled
8 STORE(rsk + "_ProviderCount", LOAD(rsk + "_ProviderCount") - 1) // Decrement the provider count

9 STORE(rsk + k, 0)
// 10 STORE(k + "_StorageCount", LOAD(k + "_StorageCount") + 1) // Increment the provider storage count
100 RETURN 0
101 RETURN 1
102 RETURN 2
103 RETURN 3
End Function

// Validator functions -----------------------------------------------------------------------
Function RegisterValidator(IPFS_CID String) Uint64
1 DIM k AS String // Create the unique identifier for the provider
2 LET k = "V_" + HEX(SHA256(SIGNER()))
3 IF EXISTS(k) == 1 THEN GOTO 11 // Validator already registered
4 STORE(k + "_IPFS_CID", IPFS_CID)
5 STORE(k + "_ValidationCount", 0)
6 STORE(k + "_wallet", SIGNER())
7 STORE(k + "_Balance", 0)
10 RETURN 0
11 RETURN 1
End Function

Function UnregisterValidator() Uint64
1 DIM k AS String
2 LET k = "V_" + HEX(SHA256(SIGNER()))
3 IF EXISTS(k) == 0 THEN GOTO 11 // Validator not registered
5 DELETE(k)
6 DELETE(k + "_IPFS_CID")
7 DELETE(k + "_ValidationCount")
8 DELETE(k + "_wallet")
9 DELETE(k + "_Balance")
10 RETURN 0
11 RETURN 1
End Function

Function WithdrawValidator() Uint64
1 DIM k AS String
2 LET k = "V_" + HEX(SHA256(SIGNER()))
3 RETURN withdraw(k)
End Function

// RS_Ks is the concatenated string of all the request UID that the validator wants to validate
// One RS_K is 8 characters long, therefore the string is a multiple of 8
// maing it possible to send up to 2300 validation at the same time
Function ValidateStorages(RS_Ks String, count Uint64) Uint64
1 DIM k AS String
2 LET k = "V_" + HEX(SHA256(SIGNER()))
3 IF EXISTS(k) == 0 THEN GOTO 101 // Validator not registered
4 IF STRLEN(RS_Ks) % 8 != 0 THEN GOTO 102 // Invalid request UID

5 MAPSTORE("rsks", RS_Ks)
6 MAPSTORE("rsks_size", count)
7 uconcat("rsks", 8)
8 DIM i AS Uint64
9 LET i = 0
10 IF i == MAPLOAD("rsks_size") THEN GOTO 100
11 validateOneStorage(MAPLOAD("vs_" + k + "_" + i))
12 LET i = i + 1
13 GOTO 10

100 RETURN 0
101 RETURN 1 // Validator not registered
102 RETURN 2 // Invalid request UID 
End Function


Function validateOneStorage(RS_K String) Uint64
1 DIM rks AS String
2 LET rks = "RS_" + RS_K
3 IF EXISTS(rks) == 0 THEN GOTO 1001 // Request Storage does not exist
4 now()
5 IF MAPLOAD("t") > LOAD(rks + "_CreatedAt") + LOAD(rks + "_Duration") THEN GOTO 100 // Request expired
6 IF MAPLOAD("t") > LOAD(rks + "_LastVerif") + 86400 THEN GOTO 200 // Validation reset, distributing rewards
7 IF LOAD(rks + "_ValidatorCout") == 0 THEN GOTO 1002 // Request already fullfilled

8 STORE(rks + "_ValidatorCout", LOAD(rks + "_ValidatorCout") - 1) // Decrement the validator count
9 STORE(rks + "_Validators", LOAD(rks + "_Validator" + ":" + RS_K) // Add the validator to the list
10 GOTO 1000

100 deleteRequest(RS_K) // Delete the request because of expiration
200 rewardRequest(RS_K) // Distribute the rewards
201 resetRequestValidation(RS_K) // Reset the request validation
1000 RETURN 0
1001 RETURN 1
1002 RETURN 2
End Function

Function deleteRequest(RS_K String) Uint64
10 return 0
End Function

Function rewardRequest(RS_K String) Uint64
1 DIM rks AS String  // Request Storage key
2 DIM i AS Uint64 // loop counter
3 DIM dailyAmount AS Uint64
4 DIM bk AS String // create a variable to store the STORE key of the provider / validator balance
5 DIM pBalance AS Uint64 // create a variable to store the provider balance
6 LET rks = "RS_" + RS_K
7 IF EXISTS(rks) == 0 THEN GOTO 1001 // Request don't exist
// 4 IF LOAD(rks + "_ValidatorCout") > 2 THEN GOTO 500 // Not enough validator
8 uconcat(rks + "_p", LOAD(rks + "_Providers"), 64)
9 uconcat(rks + "_v", LOAD(rks + "_Validators"), 64)
10 LET dailyAmount = LOAD(rks + "_InitialBounty") / (LOAD(rks + "_Duration") / 86400)

// distribute reward for the providers
100 LET i = 0
101 IF i == MAPLOAD(rks + "_p_size") THEN GOTO 200
102 LET bk = "P_" + MAPLOAD(rks + "_p_" + i) + "_Balance"
104 LET pBalance = dailyAmount / MAPLOAD(rks + "_p_size") * 0.8 // 80% of the daily amount divided by all the provider of the day
105 STORE(bk, LOAD(bk) + pBalance)
106 LET i = i + 1
107 GOTO 101

// distribute reward for the validators
200 LET i = 0
201 IF i == MAPLOAD(rks + "_v_size") THEN GOTO 1000
202 LET bk = "V_" + MAPLOAD(rks + "_v_" + i) + "_Balance"
204 LET pBalance = dailyAmount / MAPLOAD(rks + "_v_size") * 0.2 // 20% of the daily amount divided by all the provider of the day
205 STORE(bk, LOAD(bk) + pBalance)
206 LET i = i + 1
207 GOTO 201

1000 RETURN 0
End Function

Function resetRequestValidation(RS_K String) Uint64
1 DIM rks AS String
2 LET rks = "RS_" + RS_K
3 IF EXISTS(rks) == 0 THEN GOTO 11 // Request not found
4 STORE(k + "_ValidatorCout", 10)
5 STORE(k + "_Validators", "")
6 STORE(k + "_LastVerif", MAPLOAD("t"))
10 RETURN 0
11 RETURN 1
End Function


// Provider keys are 64 characters long, so maximum of 263 in-validation can be sent at once
Function InvalidateStorages(RS_Ks String, P_Ks String, count Uint64) Uint64
1 DIM k AS String
2 LET k = "V_" + HEX(SHA256(SIGNER()))
3 IF EXISTS(k) == 0 THEN GOTO 1001 // Validator not registered
4 IF STRLEN(RS_Ks) % 8 != 0 THEN GOTO 1002 // Invalid request UID
5 IF STRLEN(P_Ks) % 64 != 0 THEN GOTO 1003 // Invalid provider UID
6 MAPSTORE("rsks", RS_Ks)
7 MAPSTORE("rsks_size", count)
9 MAPSTORE("psks", P_Ks)
10 MAPSTORE("psks_size", count)
11 uconcat("rsks", RS_Ks, 8)
12 uconcat("psks", P_Ks, 64)
13 DIM i AS Uint64
14 LET i = 0
15 IF i == count THEN GOTO 1000
16 DIM rsk AS String
17 LET rsk = "RS_" + MAPLOAD("rsks_" + i)
18 DIM pks AS String
19 LET pks = "P_" + MAPLOAD("psks_" + i)
20 STORE(rsk + pks, LOAD(rsk + pks) + 1)
21 IF LOAD(rsk + pks) == 3 THEN GOTO 100 // at least three validators have marked the provider to have breach the contract.
22 LET i = i + 1
23 GOTO 15

100 // Slash the provider
101 DELETE(rsk + pks)
102 STORE(rsk + "_ProviderCount", LOAD(rsk + "_ProviderCount") + 1)
103 removeFromSArray(rsk + "_Providers", pks, LOAD(rsk + "_ProviderCount"), 64)

1000 RETURN 0
1001 RETURN 1
1002 RETURN 2
1003 RETURN 3
End Function 



// Utility function ------------------------------------------------------------------------

//I need to store a list providers and validators
// so I will store their hash as a concatenated string. They are
// represented by sha256 hashes that are 64 characters long
Function concat(k String, v String)
// If the k_size exists, increment it, otherwise create it
1 IF MAPEXISTS(k) == 0 THEN GOTO 5
2 MAPSTORE(k + "_size", MAPLOAD(k + "_size") + 1)
3 MAPSTORE(k, MAPLOAD(k) + ":" + v)
4 RETURN 0
5 MAPSTORE(k + "_size", 1)
6 MAPSTORE(k, v)
7 RETURN 0
End Function

Function uconcat(k String, s Uint64) Uint64
1 IF MAPEXISTS(k) == 0 THEN GOTO 10
2 DIM v AS String
3 DIM i AS Uint64
4 LET v = MAPLOAD(k)
5 LET i = 0
6 MAPSTORE(k + "_1", SUBSTR(v, 1*i, s))
7 LET i = i + 1
8 IF i = MAPLOAD(k + "_size") THEN GOTO 10
9 GOTO 6
10 RETURN 0
11 RETURN 1
End Function

Function removeFromRArray(k String, v String, s Uint64)
1 DIM newAKey AS String // to temporarily store the new array
2 IF MAPEXISTS(k) == 0 THEN GOTO 11 // function not ready
3 uconcat(k, s)
4 DIM i AS Uint64
5 LET i = 0
6 IF i = MAPLOAD(k + "_size") THEN GOTO 11
7 IF MAPLOAD(k + "_" + i) THEN GOTO 9
8 concat(newAKey, MAPLOAD(k + "_" + i))
9 LET i = i + 1
10 GOTO 6

11 MAPSTORE(k, MAPLOAD(newAKey))
100 RETURN 0
101 RETURN 1
End Function 

Function removeFromSArray(k String, v String, c Uint64, s Uint64)
1 MAPSTORE(k, LOAD(k))
2 MAPSTORE(k + "_size", c)
3 removeFromRArray(k, v, s)
4 STORE(k, MAPLOAD(k))
End Function 


Function now()
1 MAPSTORE("t", BLOCK_HEIGHT() + BLOCK_TIMESTAMP())
End Function

Function next(seq String)
2 STORE(seq, LOAD(seq) + 1)
End Function 

Function HEX8(v Uint64)
1 DIM s AS String
2 LET s = HEX(V)
3 IF STRLEN(s) == 8 GOTO 10
4 LET s = "0" + s
5 GOTO 3
10 MAPSTORE("h", s)
End Function 

Function withdraw(s String)
1 IF EXISTS(k) == 0 THEN GOTO 11 // Validator not registered
2 IF LOAD(k + "_wallet") != SIGNER() THEN GOTO 12 // Not the owner
3 IF LOAD(k + "_Balance") == 0 THEN GOTO 13 // Nothing to withdraw
4 SEND_DERO_TO_ADDRESS(SIGNER(), LOAD(k + "_Balance"))
5 STORE(k + "_Balance", 0)
10 RETURN 0
11 RETURN 1
12 RETURN 2
13 RETURN 3
End Function