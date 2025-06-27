#!/usr/bin/env python3
"""Level 1 Substitution (Type A): Caesar cipher.

Usage:
    python3 level1_A.py encrypt <shift> <text_file>
    python3 level1_A.py decrypt <shift> <text_file>
"""
import argparse


def caesar(text: str, shift: int) -> str:
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)


def main():
    p = argparse.ArgumentParser(description='Caesar cipher')
    p.add_argument('mode', choices=['encrypt', 'decrypt'])
    p.add_argument('shift', type=int)
    p.add_argument('text_file')
    args = p.parse_args()
    with open(args.text_file) as f:
        text = f.read()
    shift = args.shift if args.mode == 'encrypt' else -args.shift
    print(caesar(text, shift))


if __name__ == '__main__':
    main()
