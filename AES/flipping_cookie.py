import requests
from sympy import sec
from datetime import datetime, timedelta
import random
import heapq


def check_cookie(cookie, iv):
    url = f"http://aes.cryptohack.org/flipping_cookie/check_admin/{cookie}/{iv}/"
    print(url)
    r = requests.get(url)
    if r.status_code == 500:
        return {"error": True}
    r_data = r.json()
    print(r_data)
    return r_data.get("flag", None)


def get_cokie():
    url = "http://aes.cryptohack.org/flipping_cookie/get_cookie/"
    r = requests.get(url)
    r_data = r.json()
    return r_data.get("cookie", None)


cookie = get_cokie()

vi = cookie[:32]  # se sabe que vi esta al inicio del array por datos

print(vi)
print(cookie[32:])
print(len(cookie[32:]) / 32)


vi_bytes = bytes.fromhex(vi)

new_vi = vi_bytes[::]
first_block = "admin=False;expi".encode("ascii")


# Definiciones de los textos
TARGET = b"admin=True;"
first_block_content = b"admin=False;expiry={expires_at}"[:16]


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """Aplica XOR byte a byte entre dos cadenas de igual longitud."""
    return bytes(x ^ y for x, y in zip(a, b))


INITIAL_XOR_TEXT = xor_bytes(vi_bytes, first_block_content)  # Debe tener 16 bytes


def longest_common_substring(a: bytes, b: bytes) -> int:
    """
    Calcula la longitud de la subcadena (contigua) más larga en común entre dos secuencias.
    Convertimos a string usando latin-1 para mantener la correspondencia byte a byte.
    """
    s1 = a.decode("latin-1", errors="ignore")
    s2 = b.decode("latin-1", errors="ignore")
    m, n = len(s1), len(s2)
    # dp[i][j] contendrá la longitud de la subcadena terminada en s1[i-1] y s2[j-1]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    longest = 0
    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
                longest = max(longest, dp[i + 1][j + 1])
    return longest


def astar_search():
    """
    Ejecuta A* buscando un vector de 16 bytes que, al hacerle XOR con INITIAL_XOR_TEXT,
    produzca un resultado que contenga TARGET.
    La función de evaluación es: f(n) = g(n) + h(n)
      - g(n): número de cambios realizados
      - h(n): len(TARGET) - (longitud de la subcadena común más larga entre XOR_result y TARGET)
    """
    # Estado inicial: vector aleatorio de 16 bytes
    initial_state = vi_bytes[::]
    xor_initial = xor_bytes(initial_state, INITIAL_XOR_TEXT)
    h = len(TARGET) - longest_common_substring(xor_initial, TARGET)
    start = (h, 0, initial_state)  # (f, g, state)

    # Usamos una PriorityQueue implementada con heapq
    heap = [start]
    visited = set()
    visited.add(initial_state)
    iteration = 0

    while heap:
        f, g, state = heapq.heappop(heap)
        xor_result = xor_bytes(state, INITIAL_XOR_TEXT)

        # Verificamos si el resultado contiene la subcadena objetivo
        if TARGET in xor_result:
            return state

        # Generamos vecinos: modificar cada byte a cada posible valor (0-255)
        for i in range(16):
            for new_val in range(256):
                if state[i] == new_val:
                    continue  # No se considera si no hay cambio
                new_state = state[:i] + bytes([new_val]) + state[i + 1 :]
                if new_state in visited:
                    continue
                visited.add(new_state)
                new_xor = xor_bytes(new_state, INITIAL_XOR_TEXT)
                new_h = len(TARGET) - longest_common_substring(new_xor, TARGET)
                new_g = g + 1  # Un cambio más
                new_f = new_g + new_h
                heapq.heappush(heap, (new_f, new_g, new_state))

        iteration += 1
        if iteration % 1000 == 0:
            print(f"Iteración {iteration}, tamaño de la cola: {len(heap)}")

    print("No se encontró solución.")
    return None


new_vi_bytes = astar_search()
if new_vi_bytes is not None:
    resp = check_cookie(cookie[32::], new_vi_bytes.hex())
    print(resp)
