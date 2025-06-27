#!/usr/bin/env python3
"""Level 1 Transposition (Type A): simple columnar transposition cipher.

Usage:
    python3 level1_A.py encrypt <key> <text_file>
    python3 level1_A.py decrypt <key> <text_file>
"""
import argparse
import math


def encrypt(text: str, key: str) -> str:
    cols = len(key)
    rows = math.ceil(len(text) / cols)
    grid = ['' for _ in range(cols)]
    for idx, ch in enumerate(text):
        col = idx % cols
        grid[col] += ch
    order = sorted(range(cols), key=lambda i: key[i])
    return ''.join(grid[i] for i in order)


def decrypt(text: str, key: str) -> str:
    cols = len(key)
    rows = math.ceil(len(text) / cols)
    order = sorted(range(cols), key=lambda i: key[i])
    lengths = [rows] * cols
    short_cols = cols * rows - len(text)
    for i in range(short_cols):
        lengths[order[-(i + 1)]] -= 1
    chunks = {}
    pos = 0
    for idx in order:
        chunks[idx] = text[pos:pos + lengths[idx]]
        pos += lengths[idx]
    result = []
    for r in range(rows):
        for c in range(cols):
            if r < len(chunks[c]):
                result.append(chunks[c][r])
    return ''.join(result)


def main():
    p = argparse.ArgumentParser(description='Columnar transposition cipher')
    p.add_argument('mode', choices=['encrypt', 'decrypt'])
    p.add_argument('key')
    p.add_argument('text_file')
    args = p.parse_args()
    with open(args.text_file) as f:
        text = f.read().rstrip('\n')
    if args.mode == 'encrypt':
        out = encrypt(text, args.key)
    else:
        out = decrypt(text, args.key)
    print(out)


if __name__ == '__main__':
    main()
