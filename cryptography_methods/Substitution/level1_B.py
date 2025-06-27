#!/usr/bin/env python3
"""Level 1 Substitution (Type B): frequency analysis for Caesar cipher.

Usage:
    python3 level1_B.py <ciphertext>
"""
import sys
from collections import Counter

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def guess_shift(text: str) -> int:
    text = ''.join(filter(str.isalpha, text.lower()))
    if not text:
        return 0
    freq = Counter(text)
    most_common = freq.most_common(1)[0][0]
    shift = (ord(most_common) - ord('e')) % 26
    return shift


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 level1_B.py <ciphertext>')
        sys.exit(1)
    cipher = sys.argv[1]
    shift = guess_shift(cipher)
    print(f'Guessed shift: {shift}')
