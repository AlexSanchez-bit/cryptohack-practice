from typing import Tuple


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


class MongoveryCurve:
    def __init__(self, A, B, p):
        self.A = A
        self.B = B
        self.p = p

    def point_addition(
        self, point1: Tuple[int, int] | None, point2: Tuple[int, int] | None
    ):
        if point1 is None:
            return point2
        if point2 is None:
            return point1
        (x1, y1), (x2, y2) = point1, point2

        if x1 == x2 and y1 == -y2:
            return None  # Punto neutro

        alpha = (mod_inverse(x2 - x1, self.p) * (y2 - y1)) % self.p

        x3 = (self.B * pow(alpha, 2, self.p) - self.A - x1 - x2) % self.p
        y3 = (alpha * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def point_duplication(self, point: Tuple[int, int] | None):
        if point is None:
            return None
        (x, y) = point
        alpha = (
            (3 * pow(x, 2, self.p) + 2 * self.A * x + 1)
            * mod_inverse(self.B * y * 2, self.p)
        ) % self.p

        x3 = self.B * pow(alpha, 2, self.p) - self.A - 2 * x
        y3 = alpha * (x - x3) - y
        return (x3 % self.p, y3 % self.p)

    def scalar_multiplication(self, n: int, point: Tuple[int, int]):
        # Inicialización correcta: R0 = punto al infinito (representado como None), R1 = P
        R0 = None  # Elemento neutro (manejar como caso especial)
        R1 = point

        # Convierte n a binario y procesa desde el MSB (ignorando el primer 1)
        bits = bin(n)[2:]  # Ejemplo: n=13 (0b1101) → bits="101"

        for bit in bits:
            if bit == "0":
                # Actualiza R0 y R1 según el bit
                R1 = self.point_addition(R0, R1)
                R0 = self.point_duplication(R0)
            else:
                R0 = self.point_addition(R0, R1)
                R1 = self.point_duplication(R1)

        return R0 or R1  # Retorna R0 si no es None, de lo contrario R1

    def __str__(self):
        return f"{self.B}*y^2 = x^3 +{self.A}*x^2 + x  mod {self.p}"


mongovery_curve = MongoveryCurve(486662, 1, pow(2, 255) - 19)
print(mongovery_curve)
base_point_x = 9
y_2 = 9**3 + 486662 * (9**2) + 9
y = 14781619447589544791020593568409986887264606134616475288964881837755586237401

print(f"y^2={y_2} => y={y}")


n_ = b"0x1337c0decafe"

n = int("1337c0decafe", 16)

print(f"n = {n}")

my_solution = mongovery_curve.scalar_multiplication(n, (9, y))

print(f"[{n}]Q = [{n}]({9},{y}) = {my_solution}")

solution = 49231350462786016064336756977412654793383964726771892982507420921563002378152

assert solution == my_solution
