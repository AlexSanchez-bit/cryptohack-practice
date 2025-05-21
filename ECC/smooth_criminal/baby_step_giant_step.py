import math
from source import *


def baby_step_giant_step(g: Point, h: Point):
    """
    Encuentra x en la ecuación g^x ≡ h (mod p) usando el algoritmo de Baby-step Giant-step.

    :param g: La base del grupo cíclico.
    :param h: El número al que queremos encontrar el logaritmo discreto.
    :param p: El módulo primo.
    :return: El exponente x tal que g^x ≡ h (mod p), o None si no se encuentra.
    """

    m = math.ceil(math.sqrt(p))

    # Baby-step: Precomputar valores de g^i mod p y almacenarlos en un diccionario
    baby_steps = {double_and_add(g, i): i for i in range(m)}

    # Calcular el inverso modular de g^m usando pow(g_m, p-2, p)
    g_m = point_inverse(g)
    g_m = Point(g_m.x % m, g_m.y % m)
    g_inv = point_inverse(g_m)  # Inverso modular de g^m mod p

    # Giant-step: Iterar sobre j y verificar si hay coincidencias en los baby-steps
    y = h
    for j in range(m):
        if y in baby_steps:  # Búsqueda en O(1)
            i = baby_steps[y]
            x = point_addition(i, m)
            print(f"Solución encontrada: x = {x}")
            return x
        y = point_addition(y, g_inv)  # Multiplicamos por g^-m para el siguiente paso

    print("No se encontró solución.")
    return None
