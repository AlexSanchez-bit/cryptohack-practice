import requests


def encrypt(plaintext):
    plain_hex = plaintext.encode().hex()
    url = "http://aes.cryptohack.org/ecb_oracle/encrypt/" + plain_hex
    r = requests.get(url)
    r_data = r.json()
    return r_data.get("ciphertext", None)


if __name__ == "__main__":
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_{}!"
    flag = ""

    while flag[-1:] != "}":
        for guess in letters:
            padded_guess = "A" * (16 - (len(flag) + 1) % 16) + flag + guess
            to_encrypt = "A" * (16 - (len(flag) + 1) % 16)
            # print(padded_guess)
            # print(to_encrypt)
            encrypted = encrypt(padded_guess + to_encrypt)
            # print(encrypted[:32])
            # print(encrypted[32:64])
            if encrypted[0:32] == encrypted[32:64]:
                flag += guess
                print("flag: " + flag)
                break
