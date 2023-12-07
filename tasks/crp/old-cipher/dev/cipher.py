from typing import List
import argparse

from Crypto.Util.Padding import pad, unpad

class Cipher:
    key: bytes
    ROUNDS: int = 15
    PBOX: List[int] = [10, 3, 6, 9, 4, 8, 0, 13, 11, 2, 7, 15, 14, 1, 5, 12]
    SBOX: List[int] = [
            42, 43, 40, 41, 46, 47, 44, 45, 34, 35, 32, 33, 38, 39, 36, 37, 58,
            59, 56, 57, 62, 63, 60, 61, 50, 51, 48, 49, 54, 55, 52, 53, 10, 11,
            8, 9, 14, 15, 12, 13, 2, 3, 0, 1, 6, 7, 4, 5, 26, 27, 24, 25, 30,
            31, 28, 29, 18, 19, 16, 17, 22, 23, 20, 21, 106, 107, 104, 105,
            110, 111, 108, 109, 98, 99, 96, 97, 102, 103, 100, 101, 122, 123,
            120, 121, 126, 127, 124, 125, 114, 115, 112, 113, 118, 119, 116,
            117, 74, 75, 72, 73, 78, 79, 76, 77, 66, 67, 64, 65, 70, 71, 68,
            69, 90, 91, 88, 89, 94, 95, 92, 93, 82, 83, 80, 81, 86, 87, 84, 85,
            170, 171, 168, 169, 174, 175, 172, 173, 162, 163, 160, 161, 166,
            167, 164, 165, 186, 187, 184, 185, 190, 191, 188, 189, 178, 179,
            176, 177, 182, 183, 180, 181, 138, 139, 136, 137, 142, 143, 140,
            141, 130, 131, 128, 129, 134, 135, 132, 133, 154, 155, 152, 153,
            158, 159, 156, 157, 146, 147, 144, 145, 150, 151, 148, 149, 234,
            235, 232, 233, 238, 239, 236, 237, 226, 227, 224, 225, 230, 231,
            228, 229, 250, 251, 248, 249, 254, 255, 252, 253, 242, 243, 240,
            241, 246, 247, 244, 245, 202, 203, 200, 201, 206, 207, 204, 205,
            194, 195, 192, 193, 198, 199, 196, 197, 218, 219, 216, 217, 222,
            223, 220, 221, 210, 211, 208, 209, 214, 215, 212, 213
            ]
    INV_PBOX: List[int] = [6, 13, 9, 1, 4, 14, 2, 10, 5, 3, 0, 8, 15, 7, 12, 11]

    def __init__(self, key: bytes):
        self.key = key

    def encrypt(self, data: bytes) -> bytes:
        data = pad(data, 16)
        encrypted = b''
        for i in range(0, len(data), 16):
            encrypted += self.encrypt_block(data[i : i+16])

        return encrypted

    def decrypt(self, encrypted: bytes) -> bytes:
        data = b''
        for i in range(0, len(encrypted), 16):
            data += self.decrypt_block(encrypted[i : i+16])

        return unpad(data, 16)

    def encrypt_block(self, block: bytes) -> bytes:
        encrypted_block = bytearray(block)
        for round in range(self.ROUNDS):
            for i in range(16):
                encrypted_block[i] ^= self.key[i]
            for i in range(16):
                encrypted_block[i] = self.SBOX[encrypted_block[i]]
            encrypted_block = bytearray(encrypted_block[i] for i in self.PBOX)

        return bytes(encrypted_block)

    def decrypt_block(self, block: bytes) -> bytes:
        encrypted_block = bytearray(block)
        for round in range(self.ROUNDS):
            encrypted_block = bytearray(encrypted_block[i] for i in self.INV_PBOX)
            for i in range(16):
                encrypted_block[i] = self.SBOX[encrypted_block[i]]
            for i in range(16):
                encrypted_block[i] ^= self.key[i]

        return bytes(encrypted_block)


def main():
    parser = argparse.ArgumentParser(
                    prog='cryptor',
                    description='encrypts or decrypts file',
                    epilog='kek')

    parser.add_argument('key')
    parser.add_argument('action', choices=["encrypt", "decrypt"])
    parser.add_argument('in_file_name')
    parser.add_argument('out_file_name')

    args = parser.parse_args()

    cipher = Cipher(args.key.encode())

    with open(args.in_file_name, 'rb') as in_file, open(args.out_file_name, 'wb') as out_file:
        if args.action == "encrypt":
            action = cipher.encrypt
        else:
            action = cipher.decrypt
        out_file.write(action(in_file.read()))

if __name__ == "__main__":
    main()
