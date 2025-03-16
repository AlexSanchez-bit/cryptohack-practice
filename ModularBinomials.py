from math import gcd
from utils.extract_data import parse_data_file
import sys
import gmpy2
from sympy import factorint


def main():
    # Extraemos los datos del archivo data.txt
    data = parse_data_file("data_modular_binomials.txt")
    required_keys = ["N", "c1", "c2", "e1", "e2"]
    if not all(key in data for key in required_keys):
        print("Error: El archivo data.txt debe contener N, c1, c2, e1 y e2.")
        sys.exit(1)

    N = data["N"]
    c1 = data["c1"]
    c2 = data["c2"]
    e1 = int(data["e1"])
    e2 = int(data["e2"])

    a1 = 2
    a2 = 5
    b1 = 3
    b2 = 7

    inversea1 = pow(a1, -e1 * e2, N)
    inversea2 = pow(a2, -e1 * e2, N)

    inverseb1 = pow(b1, -e1 * e2, N)
    inverseb2 = pow(b2, -e1 * e2, N)

    q_dif = inversea1 * pow(c1, e2, N) - inversea2 * pow(c2, e1, N)
    p_dif = inverseb1 * pow(c1, e2, N) - inverseb2 * pow(c2, e1, N)

    q = gcd(N, q_dif)
    p = gcd(N, p_dif)
    print(f"crypto{'{'}{p},{q}{'}'}")


if __name__ == "__main__":
    main()
