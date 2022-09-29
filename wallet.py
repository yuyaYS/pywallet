from ecdsa import NIST256p
from ecdsa import SigningKey
import base58
import codecs
import hashlib


class Wallet(object):
    def __init__(self) -> None:
        self._private_key = SigningKey.generate(curve = NIST256p)
        self._public_key =self._private_key.get_verifying_key()

    @property
    def private_key(self):
        return self._private_key.to_string().hex()

    @property
    def public_key(self):
        return self._public_key.to_string().hex()


    def generate_blockchain_address(self):
        public_key_bytes = self._public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()

        ripemed160_bpk = hashlib.new('ripemd160')
        ripemed160_bpk.update(sha256_bpk_digest)
        ripemed160_bpk_digest = ripemed160_bpk.digest()
        ripemed160_bpk_hex = codecs.encode(ripemed160_bpk_digest, 'hex')

if __name__=='__main__':
    wallet = Wallet()
    print(wallet.private_key)
    print(wallet.public_key)