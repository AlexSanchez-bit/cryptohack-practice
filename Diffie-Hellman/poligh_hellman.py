import math
from sympy import factorint
from sympy.ntheory.modular import crt


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
            print(f"Solución encontrada: x = {x}")
            return x
        y = (y * g_inv) % p  # Multiplicamos por g^-m para el siguiente paso

    print("No se encontró solución.")
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
