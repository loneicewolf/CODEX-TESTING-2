#!/usr/bin/env python3
"""Level 2 Transposition (Type B): attempt to brute-force Scytale circumference.

Usage:
    python3 level2_B.py <ciphertext> [max_circumference]
"""
import sys

from string import printable


def decrypt(text: str, circumference: int) -> str:
    rows = circumference
    cols = (len(text) + rows - 1) // rows
    grid = [[''] * cols for _ in range(rows)]
    idx = 0
    for c in range(cols):
        for r in range(rows):
            if idx < len(text):
                grid[r][c] = text[idx]
                idx += 1
    result = []
    for r in range(rows):
        result.extend(grid[r])
    return ''.join(result).rstrip()


def brute_force(ciphertext: str, max_circ: int):
    for circ in range(2, max_circ + 1):
        plain = decrypt(ciphertext, circ)
        if all(c in printable for c in plain):
            print(f'circumference {circ}: {plain[:50]}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 level2_B.py <ciphertext> [max_circumference]')
        sys.exit(1)
    cipher = sys.argv[1]
    max_circ = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    brute_force(cipher, max_circ)
