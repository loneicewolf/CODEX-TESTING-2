#!/usr/bin/env python3
"""Level 2 Substitution (Type B): naive attack on Vigenere cipher using known key length.

Usage:
    python3 level2_B.py <ciphertext> <key_length>
"""
import sys
from collections import Counter

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def guess_key(cipher: str, key_len: int) -> str:
    cipher = ''.join(filter(str.isalpha, cipher.lower()))
    key = []
    for i in range(key_len):
        segment = cipher[i::key_len]
        freq = Counter(segment)
        most = freq.most_common(1)[0][0]
        shift = (ord(most) - ord('e')) % 26
        key.append(ALPHABET[shift])
    return ''.join(key)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 level2_B.py <ciphertext> <key_length>')
        sys.exit(1)
    cipher = sys.argv[1]
    key_len = int(sys.argv[2])
    key = guess_key(cipher, key_len)
    print(f'Guessed key: {key}')
