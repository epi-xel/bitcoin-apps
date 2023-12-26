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
    # post_tx(solution_ex1)  # TODO uncomment this line if you want to post the transaction to the testnet

    ### Exercise 2
    solution_ex2 = solve_ex2(TX_IN_EX2, CAROL, 2500)
    print_tx(solution_ex2, 'Transaction solution_ex2')
    # post_tx(solution_ex2)  # TODO uncomment this line if you want to post the transaction to the testnet

    ### Exercise 3
    solution_ex3 = solve_ex3(TX_IN_EX3, DAVE, 4000)
    print_tx(solution_ex3, 'Transaction solution_ex3')
    # post_tx(solution_ex3)  # TODO uncomment this line if you want to post the transaction to the testnet

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
    tx_in.script_sig = Script(['OP_0']) # TODO replace 'OP_0' with your solution here

    return tx

def solve_ex2(tx_in: TxInput, id_carol: Id, amount: int) -> Transaction:  # You can modify the parameters if you need to
    #### Create outputs
    tx_out = TxOutput(amount, id_carol.p2pkh)

    #### Create transaction
    tx = Transaction([tx_in], [tx_out])

    #### Create signature(s)
    sig_carol = id_carol.sk.sign_input(tx, 0, SCRIPT_PK_EX2)

    #### Set unlocking script (script_sig) to match the locking script (script_pk) of the given input 
    tx_in.script_sig = Script(['OP_0']) # TODO replace 'OP_0' with your solution here

    return tx

def solve_ex3(tx_in: TxInput, id_dave: Id, amount: int) -> Transaction:  # You can modify the parameters if you need to
    #### Create outputs
    tx_out = TxOutput(amount, id_dave.p2pkh)

    #### Create transaction
    tx = Transaction([tx_in], [tx_out])

    #### Create signature(s)
    sig_dave = id_dave.sk.sign_input(tx, 0, SCRIPT_PK_EX3)
    
    #### Set unlocking script (script_sig) to match the locking script (script_pk) of the given input 
    tx_in.script_sig = Script(['OP_O']) # TODO replace 'OP_0' with your solution here

    return tx

if __name__ == "__main__":
    main()
