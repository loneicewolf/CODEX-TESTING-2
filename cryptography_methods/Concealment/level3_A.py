#!/usr/bin/env python3
"""Level 3 Concealment (Type A): AES-encrypted LSB steganography.

Requires Pillow and PyCryptodome.

Usage:
    python3 level3_A.py hide <input_png> <text_file> <password> <output_png>
    python3 level3_A.py extract <stego_png> <password>
"""
import argparse
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image


BLOCK_SIZE = 16


def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()


def _to_bits(data: bytes):
    for byte in data:
        for i in range(8):
            yield (byte >> (7 - i)) & 1


def hide(input_png: str, text_file: str, password: str, output_png: str) -> None:
    with open(text_file, 'rb') as f:
        plaintext = f.read()
    key = derive_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.iv + cipher.encrypt(pad(plaintext, BLOCK_SIZE)) + b'\0'

    img = Image.open(input_png)
    pixels = img.load()
    width, height = img.size
    bits = list(_to_bits(ciphertext))
    if len(bits) > width * height:
        raise ValueError('Message too large for image')
    idx = 0
    for y in range(height):
        for x in range(width):
            if idx >= len(bits):
                break
            r, g, b = pixels[x, y]
            pixels[x, y] = (r & ~1 | bits[idx], g, b)
            idx += 1
        if idx >= len(bits):
            break
    img.save(output_png)


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


def main():
    p = argparse.ArgumentParser(description='AES encrypted LSB steganography')
    sub = p.add_subparsers(dest='cmd', required=True)

    h = sub.add_parser('hide')
    h.add_argument('input_png')
    h.add_argument('text_file')
    h.add_argument('password')
    h.add_argument('output_png')

    e = sub.add_parser('extract')
    e.add_argument('stego_png')
    e.add_argument('password')

    args = p.parse_args()
    if args.cmd == 'hide':
        hide(args.input_png, args.text_file, args.password, args.output_png)
    else:
        msg = extract(args.stego_png, args.password)
        sys.stdout.buffer.write(msg)


if __name__ == '__main__':
    import sys
    main()
