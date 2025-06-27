#!/usr/bin/env python3
"""Level 2 Concealment (Type B): extract text from LSB-stego PNG images.

Usage:
    python3 level2_B.py <stego_png>
"""
import sys
from PIL import Image


def extract(stego_png: str) -> bytes:
    img = Image.open(stego_png)
    pixels = img.load()
    width, height = img.size
    bits = []
    for y in range(height):
        for x in range(width):
            bits.append(pixels[x, y][0] & 1)
    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        if byte == 0:
            break
        out.append(byte)
    return bytes(out)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 level2_B.py <stego_png>')
        sys.exit(1)
    sys.stdout.buffer.write(extract(sys.argv[1]))
