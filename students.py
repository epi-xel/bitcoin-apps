import random
import secrets
import time
import math
import requests
from typing import Tuple, List
from bitcoinutils.constants import SATOSHIS_PER_BITCOIN
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.script import Script
from identity import Id
from helper import print_tx, sha256, post_tx
from scripts import SCRIPT_PK_EX1, SCRIPT_PK_EX2, SCRIPT_PK_EX3
from parameters import ALICE, BOB, CAROL, DAVE, PUNISH_SECRET, PUNISH_HASH, UNKNOWN_HASH, TX_IN_EX1, TX_IN_EX2, TX_IN_EX3
from consts import PUNISH_TIME, FUTURE_TIME, MALLORY_PK_HASH


def main():
    ### Exercise 1
    solution_ex1 = solve_ex1(TX_IN_EX1, ALICE, BOB, 1000, 2000)
    print_tx(solution_ex1, 'Transaction solution_ex1')
    post_tx(solution_ex1)  # TODO uncomment this line if you want to post the transaction to the testnet

    # https://live.blockcypher.com/btc-testnet/tx/31e1aacd10835b2fca31c6bdeaa7037deeb20a370ec10927b2f199750c4e70e7/

    ### Exercise 2
    solution_ex2 = solve_ex2(TX_IN_EX2, CAROL, 2500)
    print_tx(solution_ex2, 'Transaction solution_ex2')
    post_tx(solution_ex2)  # TODO uncomment this line if you want to post the transaction to the testnet

    # https://live.blockcypher.com/btc-testnet/tx/0956a92892681d16f3084083e3c57652bebde75e5fa572c2f48d9fa855b8fbef/

    ### Exercise 3
    solution_ex3 = solve_ex3(TX_IN_EX3, DAVE, 4000)
    print_tx(solution_ex3, 'Transaction solution_ex3')
    post_tx(solution_ex3)  # TODO uncomment this line if you want to post the transaction to the testnet

    # https://live.blockcypher.com/btc-testnet/tx/b921fccb09b7a01d915ff557e0a15d1b905bfd2ff6406aaec202c204bfc157a4/

def solve_ex1(tx_in: TxInput, id_alice: Id, id_bob: Id, amount_alice: int, amount_bob: int) -> Transaction:  # You can modify the parameters if you need to
    #### Create outputs
    tx_out1 = TxOutput(amount_alice, id_alice.p2pkh)
    tx_out2 = TxOutput(amount_bob, id_bob.p2pkh)

    #### Create transaction
    tx = Transaction([tx_in], [tx_out1,tx_out2])

    #### Create signature(s)
    sig_alice = id_alice.sk.sign_input(tx, 0, SCRIPT_PK_EX1)
    sig_bob = id_bob.sk.sign_input(tx, 0, SCRIPT_PK_EX1)

    #### Set unlocking script (script_sig) to match the locking script (script_pk) of the given input 
    tx_in.script_sig = Script(['OP_0', 
                               sig_alice, 
                               sig_bob])

    print(tx)
    print(id_alice.addr)
    print(id_bob.addr)

    return tx

def solve_ex2(tx_in: TxInput, id_carol: Id, amount: int) -> Transaction:  # You can modify the parameters if you need to
    #### Create outputs
    tx_out = TxOutput(amount, id_carol.p2pkh)

    #### Create transaction
    tx = Transaction([tx_in], [tx_out])

    #### Create signature(s)
    sig_carol = id_carol.sk.sign_input(tx, 0, SCRIPT_PK_EX2)

    #### Set unlocking script (script_sig) to match the locking script (script_pk) of the given input 
    tx_in.script_sig = Script([sig_carol,
                               id_carol.pk.to_hex(), 
                               PUNISH_SECRET,
                               'OP_1']) 
    
    print(tx)
    print(id_carol.addr)

    return tx

def solve_ex3(tx_in: TxInput, id_dave: Id, amount: int) -> Transaction:  # You can modify the parameters if you need to
    #### Create outputs
    tx_out = TxOutput(amount, id_dave.p2pkh)

    #### Create transaction
    tx = Transaction([tx_in], [tx_out])

    #### Create signature(s)
    sig_dave = id_dave.sk.sign_input(tx, 0, SCRIPT_PK_EX3)
    
    #### Set unlocking script (script_sig) to match the locking script (script_pk) of the given input 
    tx_in.script_sig = Script([sig_dave,
                               id_dave.pk.to_hex(),
                               'OP_0',
                               'OP_0',
                               sig_dave,
                               id_dave.pk.to_hex()])

    print(tx)
    print(id_dave.addr)

    return tx

if __name__ == "__main__":
    main()
