import requests
from sympy import sec
import random


def encrypt_block(plain_hex, iv):
    url = "http://aes.cryptohack.org/symmetry/encrypt/" + plain_hex + f"/{iv}"
    print(url)
    r = requests.get(url)
    print(r.text)
    r_data = r.json()
    return r_data.get("ciphertext", None)


def encrypt_flag():
    url = "http://aes.cryptohack.org/symmetry/encrypt_flag/"
    r = requests.get(url)
    r_data = r.json()
    return r_data.get("ciphertext", None)


cypher = encrypt_flag()

vi = cypher[:32]  # se sabe que vi esta al inicio del array por datos

flag = cypher[32:]

print(flag)

random_block = f"{flag}"

encrypted_random = encrypt_block(random_block, vi)

vi_bytes = bytes.fromhex(vi)
encryped_random_block_bytes = bytes.fromhex(encrypted_random)
random_block_bytes = bytes.fromhex(random_block)

xored_bytes = bytes(
    [b1 ^ b2 for b1, b2 in zip(encryped_random_block_bytes, random_block_bytes)]
)

print(xored_bytes.hex())

flag_bytes = bytes.fromhex(flag)

flag_bytes = bytes([b1 ^ b2 for b1, b2 in zip(flag_bytes, xored_bytes)])

decrypted_flag = flag_bytes.hex()

print(flag_bytes.decode("ascii"))
