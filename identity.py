from bitcoinutils.keys import P2pkhAddress, PrivateKey, PublicKey
import init
import consts

init.initNetwork()

class Id:
    """
    Helper class for handling identity related keys and addresses easily
    """
    def __init__(self, sk: PrivateKey):
        self.sk = sk
        self.pk = self.sk.get_public_key()
        self.addr = self.pk.get_address().to_string()
        self.p2pkh = P2pkhAddress(self.addr).to_script_pub_key()

    @classmethod
    def from_hexstring(cls, sk: str):
        return Id(PrivateKey(secret_exponent=int(sk,16)))

    @classmethod
    def from_int(cls, sk: str):
        return Id(PrivateKey(secret_exponent=sk))

    def get_sk_hex(self) -> str:
        return self.sk.to_bytes().hex()

    def get_pk_hash(self):
        #print(self.pk.to_hash160())
        #print(P2pkhAddress(self.addr).to_hash160())
        #return self.pk.to_hash160()
        return P2pkhAddress(self.addr).to_hash160()