import re


def parse_data_file(filename):
    """
    Lee el archivo de datos y extrae las variables
    Se espera que cada línea tenga el formato: variable = número
    """
    values = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            # Ignorar líneas vacías o comentarios
            if not line or line.startswith("#"):
                continue
            # Se usa regex para extraer la variable y el número
            match = re.match(r"(\w+)\s*=\s*(\d+)", line)
            if match:
                key, num = match.groups()
                values[key] = int(num)
    return values
