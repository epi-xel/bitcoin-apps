## Cryptocurrencies WS2023 - Task 6a - Payment Channels

Author: Elisa Pioldi

# Exercise 1

### Script

`OP_0` `<sigAlice>` `<sigBob>`

### Explanation

First, let's look at the locking script used with the unlocking one to verify the transaction:

`OP_2` `<pubKeyAlice>`  `<pubKeyBob>` `OP_2` `CHECKMULTISIG`

`CHECKMULTISIG` compares the first signature against each public key until it finds an ECDSA match: it requires to put the number of signatures and public keys on the stack after the signatures and public keys themselves. In this case, the number of signatures and public keys is 2, so we have to put `OP_2` before the signatures and public keys.

I had to just add `OP_0` before the signatures and the signatures themselves to complete the unlocking script: `OP_0` is used to contrast the bug of `CHECKMULTISIG` that pops an extra element off the stack.

### Bonus question

# Exercise 2

### Script

`<sigCarol>` `<pubKeyCarol>` `<punishSecret>` `OP_1`

### Explanation

First, let's look at the locking script used with the unlocking one to verify the transaction:

`OP_IF` `OP_SHA256` `<punishHash>` `OP_EQUALVERIFY` `OP_DUP` `OP_HASH160` `<pubKeyCarolHash>` `OP_ELSE` `<punishTime>` `OP_CHECKSEQUENCEVERIFY` `OP_DROP` `OP_DUP` `OP_HASH160` `<pubKeyMalloryHash>` `OP_ENDIF` `OP_EQUALVERIFY` `OP_CHECKSIG`

`OP_IF` and `OP_ELSE` are used to create a conditional statement. `OP_IF` pops the top stack item and executes the statements if it is not False. `OP_ELSE` executes the statements if the preceding `OP_IF` was not executed. `OP_ENDIF` terminates the conditional statement.

In our case, Carol has to punish Mallory for misbehaving. For this reason, we have to execute the statements in the first branch of the conditional statement. In particular, we have to execute the statements in the first branch of the conditional statement if the top stack item is not False: this means that we have to put `OP_1` in the unlocking script.
Moreover, in the branch there is an `OP_EQUALVERIFY` that pops the top two stack items and verifies that they are equal. In this case, the top two stack items are the `<punishHash>` and the hash of the value before it in the stack: to make it work, we have to put `<punishSecret>` in the unlocking script.
Finally, we have to put `<sigCarol>` and `<pubKeyCarol>` in the unlocking script to complete it, since at the end of the locking script there are `OP_EQUALVERIFY` and `OP_CHECKSIG` that pop the top two stack items and verify that the provided signature matches the provided public key.

### Bonus question

# Exercise 3

### Script

`<sigDave>` `<pubKeyDave>` `OP_0` `OP_0` `<sigDave>` `<pubKeyDave>`

### Explanation

First, let's look at the locking script used with the unlocking one to verify the transaction:
    
```
OP_DUP OP_HASH160 <pubKeyDaveHash> OP_EQUALVERIFY OP_CHECKSIGVERIFY
OP_IF
    <futureTime> OP_CHECKLOCKTIMEVERIFY OP_DROP OP_DUP OP_HASH160 <pubKeyDaveHash>
OP_ELSE
    OP_SHA256 <unknownHash> OP_EQUAL OP_2DUP OP_HASH160 <pubKeyMalloryHash> OP_2ROT OP_DUP OP_DUP
OP_ENDIF
OP_EQUALVERIFY OP_CHECKSIGVERIFY OP_2DROP OP_DROP OP_NOT
```

We know that there are some bugs that let us retrieve the money before the time specified in the locking script.

First of all, we have to put `<sigDave>` and `<pubKeyDave>` at the top of the stack in the unlocking script to complete it, since at the start of the locking script there are `OP_EQUALVERIFY` and `OP_CHECKSIGVERIFY` that pop the top two stack items and verify that the provided signature matches the provided public key. At this point we leave in the stack `<sigDave>` `<pubKeyDave>`, which will be used later.

Looking at the conditional statement, if we execute the statements in the second branch, the time specified in the locking script is not checked. For this reason, I put `OP_0` in the unlocking script to put a 0 at the top of the stack.

Executing the statements in the second branch, we need to hash the value before it in the stack and compare it with the `<unknownHash>` in the locking script. I put `OP_0` in the unlocking script which will be hashed (and will be used for the last operation in the stack): `OP_EQUAL` comparing the unknown hash with the hash of 0 will return False: now in the stack we have `<sigDave>` `<pubKeyDave>` and the value 0.
The next operation is `OP_2DUP` that duplicates the top two stack items. In this case, the top two stack items are `<pubKeyDave>` and the value 0: after the operation, in the stack we have:

`<sigDave>` `<pubKeyDave>` `0` `<pubKeyDave>` `0`

We hash the last value and we add `<pubKeyMalloryHash>` to the stack:

`<sigDave>` `<pubKeyDave>` `0` `<pubKeyDave>` `<0Hash>` `<pubKeyMalloryHash>`

Then we have the operation `OP_2ROT` that moves the third and fourth items in the stack to the top. In this case, the third and fourth items are `<pubKeyDave>` and `<0Hash>`: after the operation, in the stack we have:

`0` `<pubKeyDave>` `<0Hash>` `<pubKeyMalloryHash>` `<sigDave>` `<pubKeyDave>`  

We duplicate twice the top stack item (`OP_DUP` `OP_DUP`):

`0` `<pubKeyDave>` `<0Hash>` `<pubKeyMalloryHash>` `<sigDave>` `<pubKeyDave>` `<pubKeyDave>` `<pubKeyDave>`

Outside the condition statement, we have `OP_EQUALVERIFY` and we check that the last two stack items are equal. In this case, the last two stack items are `<pubKeyDave>` and `<pubKeyDave>`: the operation returns True and the two items are popped from the stack.

`OP_CHECKSIGVERIFY` pops the top two stack items and verifies that the provided signature matches the provided public key. In this case, the top two stack items are `<sigDave>` and `<pubKeyDave>`: the operation returns True and the two items are popped from the stack.

`OP_2DROP` pops the top two stack items. In this case, the top two stack items are `<pubKeyMalloryHash>` and `<0Hash>`.

`OP_DROP` pops the top stack item. In this case, the top stack item is `<pubKeyDave>`.

Last, `OP_NOT` pops the top stack item and returns True if it is False. In this case, the top stack item is 0: the operation leaves True in the stack and the transaction is valid.