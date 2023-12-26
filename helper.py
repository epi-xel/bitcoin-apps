import binascii
import hashlib
from bitcoinutils.transactions import Transaction
import requests
import time
from consts import API_SEND_ENDPOINT, API_SEND_ENDPOINT2

def hash256(hexstring: str) -> str:
    return sha256(sha256(hexstring))

def sha256(hexstring: str) -> str:
    data = binascii.unhexlify(hexstring)
    return hashlib.sha256(data).hexdigest()

def print_tx(tx: Transaction, name: str) -> None:
    print(f'{name}: {int(len(tx.serialize())/2)} Bytes')
    print(tx.serialize())
    print('----------------------------------')

def post_tx(tx: Transaction):
    # response = requests.post(API_SEND_ENDPOINT, tx.serialize())  # blockstream
    response = requests.post(API_SEND_ENDPOINT2, f'{{"tx":"{tx.serialize()}"}}')  # blockcypher
    time.sleep(1.5)
    print(response.text)