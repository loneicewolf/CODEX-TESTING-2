#!/usr/bin/env python3
"""Level 3 Substitution (Type B): dictionary attack against AES-encrypted file.

Usage:
    python3 level3_B.py <cipher_file> <wordlist>
"""
import sys
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

BLOCK_SIZE = 16


def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()


def try_decrypt(cipher_data: bytes, password: str) -> bytes:
    key = derive_key(password)
    iv = cipher_data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        return unpad(cipher.decrypt(cipher_data[16:]), BLOCK_SIZE)
    except ValueError:
        return b''


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 level3_B.py <cipher_file> <wordlist>')
        sys.exit(1)
    with open(sys.argv[1], 'rb') as cf:
        cipher_data = cf.read()
    with open(sys.argv[2]) as wf:
        words = [w.strip() for w in wf]
    for word in words:
        plain = try_decrypt(cipher_data, word)
        if plain:
            print(f'Password found: {word}')
            sys.stdout.buffer.write(plain)
            break
