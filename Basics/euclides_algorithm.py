def extended_gcd(a, b):
    if b == 0:
        # Caso base: cuando b es 0, el mcd es a, y los coeficientes son 1 y 0.
        return a, 1, 0
    else:
        # Llamada recursiva
        gcd, x1, y1 = extended_gcd(b, a % b)
        # Actualizamos x e y usando los resultados de la recursión.
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y


print(extended_gcd(991, 209))
