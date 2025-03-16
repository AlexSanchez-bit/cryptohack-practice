p = 28151


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


founded = False
for element in range(2, p):
    if pow(element, p - 1, p) == 1 and not founded:
        founded_order = -1
        for exponent in range(1, p - 1):
            if gcd(exponent, p - 1) != 1:
                if pow(element, exponent, p) == 1:
                    founded_order = exponent
                    break
        if founded_order == -1:
            print(element)
            founded = True
