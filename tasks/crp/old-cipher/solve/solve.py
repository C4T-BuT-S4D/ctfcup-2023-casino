from typing import List

from Crypto.Util.Padding import unpad

PNG_HEADER = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"

ROUNDS: int = 15
PBOX: List[int] = [10, 3, 6, 9, 4, 8, 0, 13, 11, 2, 7, 15, 14, 1, 5, 12]
INV_PBOX: List[int] = [6, 13, 9, 1, 4, 14, 2, 10, 5, 3, 0, 8, 15, 7, 12, 11]

def apply_pbox(pbox, data: bytes):
    for i in range(ROUNDS):
        data = [data[i] for i in pbox]
    return bytes(data)


def main():
    with open("image.png.enc", 'rb') as f:
        encrypted = f.read()

    first_block = encrypted[:16]
    pboxed_first_block = bytearray(apply_pbox(INV_PBOX, first_block))
    xor_key = bytearray()
    for i, b in enumerate(pboxed_first_block):
        xor_key.append(b ^ 42 ^ PNG_HEADER[i]) 

    data = b''
    for i in range(0, len(encrypted), 16):
        data += bytes(k ^ b ^ 42 for k, b in zip(xor_key, apply_pbox(INV_PBOX, encrypted[i : i + 16])))

    with open("image.png", 'wb') as f:
        f.write(data)


if __name__ == "__main__":
    main()

