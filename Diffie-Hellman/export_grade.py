import pwn
import json
import hashlib
import math
from Crypto.Cipher import AES

from Crypto.Util.number import bytes_to_long


def baby_step_giant_step(g: int, h: int, p: int):
    """
    Encuentra x en la ecuación g^x ≡ h (mod p) usando el algoritmo de Baby-step Giant-step.

    :param g: La base del grupo cíclico.
    :param h: El número al que queremos encontrar el logaritmo discreto.
    :param p: El módulo primo.
    :return: El exponente x tal que g^x ≡ h (mod p), o None si no se encuentra.
    """

    m = math.ceil(math.sqrt(p))

    # Baby-step: Precomputar valores de g^i mod p y almacenarlos en un diccionario
    baby_steps = {pow(g, i, p): i for i in range(m)}

    # Calcular el inverso modular de g^m usando pow(g_m, p-2, p)
    g_m = pow(g, m, p)
    g_inv = pow(g_m, p - 2, p)  # Inverso modular de g^m mod p

    # Giant-step: Iterar sobre j y verificar si hay coincidencias en los baby-steps
    y = h
    for j in range(m):
        if y in baby_steps:  # Búsqueda en O(1)
            i = baby_steps[y]
            x = j * m + i
            return x
        y = (y * g_inv) % p  # Multiplicamos por g^-m para el siguiente paso

    print("No se encontró solución.")
    return None


host = "socket.cryptohack.org"
port = 13379


def exploit():
    pr = pwn.connect(host, port)
    try:
        pr.readuntil(": ")
        supported_methods = json.loads(pr.readline().strip().decode())
        print(supported_methods)

        pr.sendlineafter(
            ": ", json.dumps({"supported": [supported_methods["supported"][-1]]})
        )
        pr.readuntil(": ")
        selected = json.loads(pr.readline().strip().decode())
        print(selected)
        pr.sendlineafter(
            ": ", json.dumps({"chosen": supported_methods["supported"][-1]})
        )
        pr.readuntil(": ")
        peer_parameters = json.loads(pr.readline().strip().decode())
        print(peer_parameters)
        A = int((peer_parameters["A"]), 16)
        p = int(peer_parameters["p"], 16)
        g = int(peer_parameters["g"], 16)

        pr.readuntil(": ")
        line = json.loads(pr.readline().strip().decode())
        print(line)
        B = int(line["B"], 16)

        pr.readuntil(": ")
        line = json.loads(pr.readline().strip().decode())
        print(line)

        print("A", A)
        print("B", B)
        print("p", p)
        print("g", g)

        a = baby_step_giant_step(g, A, p)
        print(a)
        if a is None:
            return
        secret = pow(B, a, p)
        print("secret", secret)
        # hallar a y b decodificando la llave y desencriptar la bandera
        #

        iv = bytes.fromhex(line["iv"])
        encrypted_flag = bytes.fromhex(line["encrypted_flag"])
        sha1 = hashlib.sha1()
        sha1.update(str(secret).encode())
        key = sha1.digest()[:16]
        aes = AES.new(key, AES.MODE_CBC, iv)
        print(aes.decrypt(encrypted_flag))

    finally:
        pr.close()


exploit()
