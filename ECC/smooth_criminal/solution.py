from Crypto.Cipher import AES
from Crypto.Util.number import inverse
from Crypto.Util.Padding import pad, unpad
from collections import namedtuple
from random import randint
import hashlib
import os
from baby_step_giant_step import *
from source import *
from brute_force import *


Point = namedtuple("Point", "x y")
# data to decypher
A = Point(
    x=280810182131414898730378982766101210916, y=291506490768054478159835604632710368904
)

# Bob's public key
b_x = 272640099140026426377756188075937988094
b_y = 51062462309521034358726608268084433317
B = Point(b_x, b_y)


# usando sage discrete log
# para B
b = 23364484702955482300431942169743298535
# para A
a = 47836431801801373761601790722388100620


Secret = Point(
    171172176587165701252669133307091694084, 188106434727500221954651940996276684440
)


def encrypt_flag(shared_secret: int, iv, cipher_flag):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode("ascii"))
    key = sha1.digest()[:16]
    # Encrypt flag
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.decrypt(bytes.fromhex(cipher_flag))
    # Prepare data to send
    data = ciphertext
    return data


crypto_data = {
    "iv": "07e2628b590095a5e332d397b8a59aa7",
    "encrypted_flag": "8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af",
}


print(encrypt_flag(Secret.x, crypto_data["iv"], crypto_data["encrypted_flag"]))
