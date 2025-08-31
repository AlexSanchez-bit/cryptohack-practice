#!/usr/bin/env python3

import hashlib
import json
from pwn import remote
from Crypto.Util.number import bytes_to_long
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192
from random import randrange
import time

HOST = "socket.cryptohack.org"
PORT = 13381

# Eliptic curve parameters
g = generator_192
n = g.order()


signatures = {}


def first_call(r):
    req = {}
    r.sendline(json.dumps(req).encode())
    resp = r.recvline()
    return resp


def get_signature(r):
    """get signatures from server"""
    req = {"option":"sign_time"}
    r.sendline(json.dumps(req).encode())
    resp1 = r.recvline()
    return json.loads(resp1.decode())

def verify_signature(r,msg,r_,s):
    """verifies a signature from server"""
    req ={"option":"verify","msg":msg,"r":r_,"s":s}
    r.sendline(json.dumps(req).encode())
    resp1 = r.recvline()
    return json.loads(resp1.decode())


def sha1(data):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(data)
    return sha1_hash.digest()

def solve1():
    print("Searching for higher collission probability messages")
    r = remote(HOST, PORT)
    resp = r.recvline()
    print(resp)
    # Find a timestamp with the lowest second number
    initialTime = time.time()
    while initialTime - time.time()< 2*60:
        try:
            sig_data = get_signature(r)
            if "error" in sig_data:
                continue
            print(sig_data)
            msg = sig_data["msg"]
            s = int(sig_data["s"], 16)
            r_ = int(sig_data["r"], 16)
            seconds = int(msg.split(":")[-1])
            if seconds > 13:
                time.sleep(60 - seconds)
            elif seconds <=10:
                for i in range(1,seconds):
                    #use i as k to get private key
                    #as i know r = x(k*G) mod N and s = k^-1(hash - r*pk) mod N
                    mgs_hash = bytes_to_long(sha1(msg.encode())) #hash numeric representation of original message
                    rxPK = (s * i - mgs_hash)
                    r_inv = pow(r_,-1,n)
                    PK = r_inv * rxPK #pk is the inverse of the secret n => n*G is public key
                    pub_key = Public_key(g,g*PK)
                    priv_key = Private_key(pub_key,PK)
                    # now i know private key of the curve, lets now sign my message with that private key
                    new_message = bytes_to_long(sha1('unlock'.encode()))
                    sign = priv_key.sign(new_message,i)
                    resp = verify_signature(r,'unlock',hex(sign.r),hex(sign.s))
                    if "flag" in resp:
                        break
                    print(resp)


        except ValueError:
            print(f"error getting data: {ValueError}")
    r.close()

if __name__ == "__main__":
    print("Executing first solution attempt")
    solve1()
