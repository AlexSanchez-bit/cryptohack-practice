import requests
from sympy import sec


def decrypt(plain_hex):
    url = "http://aes.cryptohack.org/ecbcbcwtf/decrypt/" + plain_hex
    r = requests.get(url)
    r_data = r.json()
    return r_data.get("plaintext", None)


def encrypt_flag():
    url = "http://aes.cryptohack.org/ecbcbcwtf/encrypt_flag"
    r = requests.get(url)
    r_data = r.json()
    return r_data.get("ciphertext", None)


cypher = encrypt_flag()

vi = cypher[:32]  # se sabe que vi esta al inicio del array por datos

decrypted = decrypt(
    cypher[32:]
)  # desencriptamos con AES en ECB y la misma llave inicial

if len(cypher[32:]) / 32 != len(decrypted) / 32:  # se descifro mal si esto ocurre
    print(f"los bloques no son iguales {len(cypher[32:]) / 32} {len(decrypted) / 32}")


flag = ""

for block in range(1, int(len(cypher) / 32)):
    bytes1 = bytes.fromhex(decrypted[(block - 1) * 32 : block * 32])
    bytes2 = bytes.fromhex(cypher[(block - 1) * 32 : block * 32])
    block_bytes = bytes([b1 ^ b2 for b1, b2 in zip(bytes1, bytes2)])
    flag += block_bytes.hex()


bytes = bytes.fromhex(flag)
print(bytes.decode("utf-8"))
