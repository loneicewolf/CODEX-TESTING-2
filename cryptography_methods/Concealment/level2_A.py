#!/usr/bin/env python3
"""Level 2 Concealment (Type A): LSB steganography for text in PNG images.

Requires Pillow (PIL). If not installed, install via pip: pip install Pillow

Usage:
    python3 level2_A.py hide <input_png> <text_file> <output_png>
    python3 level2_A.py extract <stego_png>
"""
import argparse
from PIL import Image


def _to_bits(data: bytes):
    for byte in data:
        for i in range(8):
            yield (byte >> (7 - i)) & 1


def hide(input_png: str, text_file: str, output_png: str) -> None:
    with open(text_file, 'rb') as f:
        text = f.read() + b'\0'
    img = Image.open(input_png)
    pixels = img.load()
    width, height = img.size
    bits = list(_to_bits(text))
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


def extract(stego_png: str) -> bytes:
    img = Image.open(stego_png)
    pixels = img.load()
    width, height = img.size
    bits = []
    for y in range(height):
        for x in range(width):
            bits.append(pixels[x, y][0] & 1)
    bytes_out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        if byte == 0:
            break
        bytes_out.append(byte)
    return bytes(bytes_out)


def main():
    p = argparse.ArgumentParser(description='LSB text steganography in PNG images')
    sub = p.add_subparsers(dest='cmd', required=True)

    h = sub.add_parser('hide')
    h.add_argument('input_png')
    h.add_argument('text_file')
    h.add_argument('output_png')

    e = sub.add_parser('extract')
    e.add_argument('stego_png')

    args = p.parse_args()
    if args.cmd == 'hide':
        hide(args.input_png, args.text_file, args.output_png)
    else:
        msg = extract(args.stego_png)
        sys.stdout.buffer.write(msg)


if __name__ == '__main__':
    import sys
    main()
