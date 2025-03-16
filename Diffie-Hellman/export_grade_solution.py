import json
import hashlib
import math
from Crypto.Cipher import AES


from sympy import factorint
from sympy.ntheory.modular import crt


def baby_step_giant_step(g, h, p, n):
    """
    Encuentra x tal que g^x ≡ h (mod p) en un grupo de orden n usando BSGS.
    """
    m = math.ceil(math.sqrt(n))

    # Baby-step
    baby_steps = {pow(g, i, p): i for i in range(m)}

    # Giant-step
    g_inv = pow(g, p - 2, p)
    g_m = pow(g_inv, m, p)  # g^-m mod p
    y = h

    for j in range(m):
        if y in baby_steps:
            return j * m + baby_steps[y]
        y = (y * g_m) % p

    return None


def discrete_log_pohlig_hellman(g, h, p):
    """
    Resuelve g^x ≡ h (mod p) usando el algoritmo de Pohlig-Hellman.

    :param g: Generador del grupo.
    :param h: Elemento cuyo logaritmo queremos encontrar.
    :param p: Primo tal que el grupo es Z_p* de orden p-1.
    :return: El valor de x tal que g^x ≡ h (mod p).
    """

    # Factorizamos p-1 en sus factores primos
    factors = factorint(p - 1)  # Devuelve un diccionario {q: e}

    x_congruences = []  # Lista de soluciones x_i para cada subgrupo
    moduli = []  # Lista de los módulos q_i^{e_i}

    for q, e in factors.items():
        q_e = q**e
        g_i = pow(g, (p - 1) // q_e, p)  # g^( (p-1) / q^e ) mod p
        h_i = pow(h, (p - 1) // q_e, p)  # h^( (p-1) / q^e ) mod p

        # Resolver el logaritmo discreto en este subgrupo
        x_i = baby_step_giant_step(g_i, h_i, p, q_e)  # Resolver en este subgrupo

        x_congruences.append(x_i)
        moduli.append(q_e)

    # Resolver el sistema de congruencias con el Teorema Chino del Resto
    x, _ = crt(moduli, x_congruences)

    return x


A = 3621853669268860647
B = 10671808878731881319
p = 16007670376277647657
g = 2
line = {
    "iv": "8ff8c310ccb4a81ce7a9e1cf7485a828",
    "encrypted_flag": "14130f3c069f6930645ffb40e7b01f373c768d3a1dd676f3ecf7c36fb686a134",
}

print("A", A)
print("B", B)
print("p", p)
print("g", g)
a = discrete_log_pohlig_hellman(g, A, p)
print(a)
if a is None:
    exit()
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
