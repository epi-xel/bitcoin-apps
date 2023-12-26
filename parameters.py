from bitcoinutils.transactions import TxInput
from identity import Id
from helper import sha256

# TODO: Download your individual params.py file from TUWEL (https://tuwel.tuwien.ac.at/mod/assign/view.php?id=2152745)
from params import *


#### BEGIN generate identities, tx inputs and hash. DO NOT MODIFY 
ALICE = Id.from_hexstring(ALICE_SK)
BOB = Id.from_hexstring(BOB_SK)
CAROL = Id.from_hexstring(CAROL_SK)
DAVE = Id.from_hexstring(DAVE_SK)
TX_IN_EX1 = TxInput(TX_IN_EX1_HASH, 0)
TX_IN_EX2 = TxInput(TX_IN_EX2_HASH, 0)
TX_IN_EX3 = TxInput(TX_IN_EX3_HASH, 0)
PUNISH_HASH = sha256(PUNISH_SECRET)
#### END generate identities, tx inputs and hash. DO NOT MODIFY