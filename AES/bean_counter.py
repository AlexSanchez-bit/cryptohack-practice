import requests


def fetch_encrypted():
    url = "http://aes.cryptohack.org/bean_counter/encrypt/"
    response = requests.get(url)
    # Obtenemos la cadena hexadecimal proveniente del endpoint
    encrypted_hex = response.json()["encrypted"]
    return bytes.fromhex(encrypted_hex)


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def main():
    # Descargamos los datos cifrados
    encrypted = fetch_encrypted()

    # Definimos la cabecera del PNG conocida (16 bytes: 8 bytes de firma más 8 bytes del chunk IHDR)
    png_header = bytes(
        [
            0x89,
            0x50,
            0x4E,
            0x47,
            0x0D,
            0x0A,
            0x1A,
            0x0A,
            0x00,
            0x00,
            0x00,
            0x0D,
            0x49,
            0x48,
            0x44,
            0x52,
        ]
    )

    # Recuperamos el keystream aplicando XOR entre la cabecera conocida y el primer bloque cifrado
    keystream = xor_bytes(png_header, encrypted[:16])
    print("Keystream:", keystream.hex())

    # Desciframos cada byte usando el keystream de forma cíclica (ya que es constante)
    decrypted = bytearray()
    for i in range(len(encrypted)):
        decrypted.append(encrypted[i] ^ keystream[i % len(keystream)])

    # Guardamos la imagen descifrada en un archivo
    with open("bean_counter.png", "wb") as f:
        f.write(decrypted)

    print("Archivo 'bean_counter.png' generado con éxito.")


if __name__ == "__main__":
    main()
