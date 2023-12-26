from bitcoinutils.script import Script
from parameters import ALICE, BOB, CAROL, DAVE, PUNISH_HASH, UNKNOWN_HASH
from consts import PUNISH_TIME, FUTURE_TIME, MALLORY_PK_HASH

# Do not modify this file

SCRIPT_PK_EX1 = Script(['OP_2', ALICE.pk.to_hex(), BOB.pk.to_hex(), 'OP_2', 'OP_CHECKMULTISIG'])
SCRIPT_PK_EX2 = Script(['OP_IF', 
        'OP_SHA256', PUNISH_HASH, 'OP_EQUALVERIFY', 'OP_DUP', 'OP_HASH160', CAROL.get_pk_hash(), 
        'OP_ELSE', 
        PUNISH_TIME, 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP', 'OP_DUP', 'OP_HASH160', MALLORY_PK_HASH,
        'OP_ENDIF',
        'OP_EQUALVERIFY',
        'OP_CHECKSIG'])
SCRIPT_PK_EX3 = Script([
    'OP_DUP', 'OP_HASH160', DAVE.get_pk_hash(), 'OP_EQUALVERIFY', 'OP_CHECKSIGVERIFY',
    'OP_IF',  
        FUTURE_TIME, 'OP_CHECKLOCKTIMEVERIFY', 'OP_DROP', 'OP_DUP', 'OP_HASH160', DAVE.get_pk_hash(),
    'OP_ELSE', 
        'OP_SHA256', UNKNOWN_HASH, 'OP_EQUAL', 'OP_2DUP', 'OP_HASH160', MALLORY_PK_HASH, 'OP_2ROT', 'OP_DUP', 'OP_DUP',
    'OP_ENDIF',
    'OP_EQUALVERIFY',
    'OP_CHECKSIGVERIFY', 'OP_2DROP', 'OP_DROP', 'OP_NOT'])