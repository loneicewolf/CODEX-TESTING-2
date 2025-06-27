#!/usr/bin/env python3
"""Level 2 Transposition (Type A): Scytale cipher implementation.

Usage:
    python3 level2_A.py encrypt <circumference> <text_file>
    python3 level2_A.py decrypt <circumference> <text_file>
"""
import argparse


def encrypt(text: str, circumference: int) -> str:
    rows = circumference
    cols = (len(text) + rows - 1) // rows
    grid = [' ' * cols for _ in range(rows)]
    idx = 0
    for r in range(rows):
        row_chars = list(grid[r])
        for c in range(cols):
            if idx < len(text):
                row_chars[c] = text[idx]
                idx += 1
        grid[r] = ''.join(row_chars)
    return ''.join(''.join(grid[r][c] for r in range(rows)) for c in range(cols))


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


def main():
    p = argparse.ArgumentParser(description='Scytale cipher')
    p.add_argument('mode', choices=['encrypt', 'decrypt'])
    p.add_argument('circumference', type=int)
    p.add_argument('text_file')
    args = p.parse_args()
    with open(args.text_file) as f:
        text = f.read().rstrip('\n')
    if args.mode == 'encrypt':
        out = encrypt(text, args.circumference)
    else:
        out = decrypt(text, args.circumference)
    print(out)


if __name__ == '__main__':
    main()
