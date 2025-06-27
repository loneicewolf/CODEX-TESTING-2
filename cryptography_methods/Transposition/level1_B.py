#!/usr/bin/env python3
"""Level 1 Transposition (Type B): brute-force small keys for columnar cipher.

Usage:
    python3 level1_B.py <ciphertext> [max_key_length]
"""
import sys
import itertools


def decrypt(text: str, key: str) -> str:
    cols = len(key)
    rows = (len(text) + cols - 1) // cols
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


def brute_force(cipher: str, max_len: int = 4):
    for key_len in range(2, max_len + 1):
        for key in itertools.permutations('abcdefghijklmnopqrstuvwxyz'[:key_len], key_len):
            key_str = ''.join(key)
            plain = decrypt(cipher, key_str)
            if plain.isprintable():
                print(f'Possible key {key_str}: {plain[:50]}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 level1_B.py <ciphertext> [max_key_length]')
        sys.exit(1)
    ciphertext = sys.argv[1]
    max_len = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    brute_force(ciphertext, max_len)
