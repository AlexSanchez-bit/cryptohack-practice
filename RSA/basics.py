# euclides extendido
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


p = 857504083339712752489993810777
q = 1029224947942998075080348647219


e = 65537

N = p * q

# (N,e) llave publica

# d : d*e =1 mod phi(N) llave privada
_, d, _ = extended_gcd(e, (p - 1) * (q - 1))
print(d)


# decrypt example
# c : encrypted info with (N,e)
c = 77578995801157823671636298847186723593814843845525223303932


print(pow(c, d, N))
