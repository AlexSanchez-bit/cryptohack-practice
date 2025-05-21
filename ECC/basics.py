# Eliptic Curves

# are equations with the Weiestrass form Y^2 = X^3 + aX + b where a and b are fits 4a^2 + 27 b^2 != 0
# la suma de puntos en una curva eliptica se hace trazando una recta entre los dos puntos y tomando la interseccion de dicha recta con la curva
# en caso de sumar un punto consigo mismo se utiliza la recta tangente al punto
# para los casos donde donde la recta no intersecte la curva se define el punto O en el infinito tal que P+O =P, P - P =O
# se puede definir un producto escalar sobre el Grupo de los enteros tal que al hacer n*P se obtiene el punto P sumado consigo mismo n veces
# G(P,+) es un grupo abeliano, pues :
# se cumple que la let + (suma definida anteriormente) es una ley interna P + Q = {P+ O } (puntos de la curva o O)
# existe el inverso para cada punto
# existe el neutro O
# la operacion es conmutativa
# la operacion es asociativa
# el neutro es unico
#
# DEfiniendo la curva sobre campos finitos
# hacer todas las operaciones en lugar de en los reales, en un campo finito F_p
# es decir la curva es F_p[x,y]/(y^2 = x^3 + a*x + b && 4a^2 + 27 b^2 != 0)
#

from typing import Optional, Tuple


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(a, m):
    gcd, x, y = egcd(a, m)
    if abs(gcd) != 1:
        print(gcd)
        raise ValueError(f"no existe inverso modular para {a} y {m}")
    else:
        if x < 0:
            return m + x
        return x % m


class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        if 4 * a**2 + 27 * b**2 == 0:
            raise ValueError("the curve is not defined")
        self.pairs = []

    def finite_field_representation(self, x: int):
        return x % self.p

    def finite_field_sum(self, x: int, y: int):
        x = self.finite_field_representation(x)
        y = self.finite_field_representation(y)

        return self.finite_field_representation(x + y)

    def finite_field_mult(self, x: int, y: int):
        x = self.finite_field_representation(x)
        y = self.finite_field_representation(y)

        return self.finite_field_representation((x * y))

    def verify_ponitve(self, p: tuple[int, int]):
        [x, y] = p
        if y**2 == x**3 + self.a * x + self.b:
            return True
        return False

    def point_sum(
        self, point1: Optional[Tuple[int, int]], point2: Optional[Tuple[int, int]]
    ) -> Optional[Tuple[int, int]]:
        # El elemento neutro se representa como None
        if point1 is None:
            return point2
        if point2 is None:
            return point1

        [x1, y1] = point1
        [x2, y2] = point2

        x1 = self.finite_field_representation(x1)
        x2 = self.finite_field_representation(x2)
        y1 = self.finite_field_representation(y1)
        y2 = self.finite_field_representation(y2)

        # Caso en que los puntos sean inversos (resultado: punto en el infinito)
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None

        # Calcular la pendiente (lambda)
        if x1 == x2 and y1 == y2:
            # Duplicación de punto
            numerator = self.finite_field_sum(3 * pow(x1, 2, self.p), self.a)
            denominator = mod_inverse(2 * y1, self.p)
            lapse = self.finite_field_mult(numerator, denominator)
        else:
            # Suma de puntos distintos
            numerator = self.finite_field_sum(y2, -y1)
            denominator = mod_inverse(self.finite_field_representation(x2 - x1), self.p)
            lapse = self.finite_field_mult(numerator, denominator)

        x3 = self.finite_field_representation(pow(lapse, 2, self.p) - x1 - x2)
        y3 = self.finite_field_representation(lapse * (x1 - x3) - y1)
        return (x3, y3)

    def __str__(self):
        return f"y^2 = x^3 +{self.a}*x + {self.b} mod {self.p}"


class Ecc_curve(EllipticCurve):
    def __init__(self, a, b, p, P: tuple[int, int]):
        super().__init__(a, b, p)
        self.base_point = P
        self.pairs = []
        self.precompute_pairs()

    def precompute_pairs(self):
        # Precomputación de puntos dobles sucesivos para el método de multiplicación escalar
        point = self.base_point
        self.pairs.append(point)
        for i in range(1, 64):
            point = self.point_sum(point, point)
            self.pairs.append(point)

    def scalar_multiplication(self, n: int) -> Optional[Tuple[int, int]]:
        result = None  # Representa el elemento neutro
        i = 0
        while n > 0:
            if n & 1:
                result = self.point_sum(result, self.pairs[i])
            i += 1
            n >>= 1
        return result

    def __str__(self):
        return f"{super().__str__()} with base point {self.base_point}"


curve_61 = Ecc_curve(497, 1768, 9739, (8045, 6936))

p = (493, 5564)
q = (1539, 4742)
r = (4403, 5202)

x = (5274, 2841)
y = (8669, 740)

x_y = (1024, 4440)
x_x = (7284, 2107)

# point adition ex 2
print(
    "s = p+p+q+r = ",
    curve_61.point_sum(r, curve_61.point_sum(q, curve_61.point_sum(p, p))),
)


# scalar multiplication ex 3 test
curve_61 = Ecc_curve(497, 1768, 9739, (5323, 5438))
print("[1337]x = ", curve_61.scalar_multiplication(1337))

base = None

# for _ in range(1337):
#     base = curve_61.point_sum(base, (5323, 5438))
# print(base)

# scalar test ex 3
P = (2339, 2213)
scalar_test_curve = Ecc_curve(497, 1768, 9739, P)


base = P

for _ in range(7863):
    base = scalar_test_curve.point_sum(base, P)

print("q = [7863]p = ", scalar_test_curve.scalar_multiplication(7863))
print("q = [7863]p = ", base)


# Diffie Hellman on Elliptic Curves
# Alice and Bob pick a curve, prime and generator G
# Alice selects a random number a and computes A = aG
# Bob selects a random number b and computes B = bG
# They exchange their public keys A and B
# Then Bob computes C = aB = abG and Alice computes D = bA = abG
# C = D = abG is the shared secret
G = (1804, 5368)  # base selected point
Q_a = (815, 3190)  # alice public key
b = 1829  # bob private key

alice_bob_curve = Ecc_curve(497, 1768, 9739, Q_a)

print("Alice public key = ", Q_a)
print("Bob private key = ", b)
secret = alice_bob_curve.scalar_multiplication(b)
print("shared secret = ", secret)
import hashlib

if secret is not None:
    x, _ = secret
    sha1 = hashlib.sha1()
    sha1.update(str(x).encode())
    key = sha1.digest()
    print("the key is ", key.hex())


# using only X coordinate
print("Alice and bob curve: ", alice_bob_curve)
# Alice public
X_q_a = 4726
# bob secret
b = 6534

# coputing the y coordinate
# y^2 = X^3 + 497*X + 1768 mod 9739
y_2 = (pow(X_q_a, 3, 9739) + 497 * X_q_a + 1768) % 9739

y2_sqrt = 3452

alice_bob_curve = Ecc_curve(497, 1768, 9739, (X_q_a, y2_sqrt))

shared_secret = alice_bob_curve.scalar_multiplication(b)
print("shared secret = ", shared_secret)
