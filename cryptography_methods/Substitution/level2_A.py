#!/usr/bin/env python3
"""Level 2 Substitution (Type A): Vigenere cipher.

Usage:
    python3 level2_A.py encrypt <key> <text_file>
    python3 level2_A.py decrypt <key> <text_file>
"""
import argparse

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def transform(text: str, key: str, encrypt: bool = True) -> str:
    result = []
    key = key.lower()
    klen = len(key)
    for idx, ch in enumerate(text):
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            offset = ord(key[idx % klen]) - ord('a')
            if not encrypt:
                offset = -offset
            result.append(chr((ord(ch) - base + offset) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)


def main():
    p = argparse.ArgumentParser(description='Vigenere cipher')
    p.add_argument('mode', choices=['encrypt', 'decrypt'])
    p.add_argument('key')
    p.add_argument('text_file')
    args = p.parse_args()
    with open(args.text_file) as f:
        text = f.read()
    encrypting = args.mode == 'encrypt'
    print(transform(text, args.key, encrypting))


if __name__ == '__main__':
    main()
