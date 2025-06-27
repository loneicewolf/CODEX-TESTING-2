#!/usr/bin/env python3
"""Level 3 Concealment (Type B): extract AES-encrypted data from LSB-stego PNG
and decrypt using provided password.

Usage:
    python3 level3_B.py <stego_png> <password>
"""
import sys
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from PIL import Image

BLOCK_SIZE = 16


def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()


def extract(stego_png: str, password: str) -> bytes:
    key = derive_key(password)
    img = Image.open(stego_png)
    pixels = img.load()
    width, height = img.size
    bits = []
    for y in range(height):
        for x in range(width):
            bits.append(pixels[x, y][0] & 1)
    data = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        if byte == 0:
            break
        data.append(byte)
    iv = bytes(data[:16])
    ct = bytes(data[16:])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), BLOCK_SIZE)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 level3_B.py <stego_png> <password>')
        sys.exit(1)
    sys.stdout.buffer.write(extract(sys.argv[1], sys.argv[2]))
